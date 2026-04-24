"""
HTML Generator

Reads a template JSON (output of template_generator.py), a doc_key (for
few-shot PDFs), and one or more style profile keys, then generates HTML
documents with all placeholder labels preserved.

Optionally prepends few-shot PDF examples to improve layout fidelity.

Usage:
    python3 html_generator.py <template_json> <doc_key> [<style_key>] [--no-few-shots]

    template_json : path to template JSON (meta / required / optional)
    doc_key       : wartungsvertrag | wartungsprotokoll  (selects few-shot PDFs)
    style_key     : profile key or "all" (default: all)
                    compact_technical | table_layout | simple_form |
                    minimal_modern | quick_note | all
    --no-few-shots: skip loading few-shot PDF examples

Output files are written next to the template JSON:
    <template_stem>_<style_key>.html
    <template_stem>_<style_key>.raw.txt
"""

from __future__ import annotations

import json
import platform
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import boto3
from style_profiles import STYLE_PROFILES, StyleProfile

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"
BASE = Path(__file__).parent

if platform.system() == "Windows":
    _session = boto3.Session(profile_name="claude-bedrock", region_name=BEDROCK_REGION)
    _bedrock_client = _session.client("bedrock-runtime")
else:
    _bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

_STYLE_MAP: dict[str, StyleProfile] = {p.key: p for p in STYLE_PROFILES}

FEW_SHOT_PDFS: dict[str, list[str]] = {
    "wartungsprotokoll": [
        "few_shots/Wartungsprotokoll_Waermepumpe-1.pdf",
        "few_shots/Wartungsprotokoll-Rauchwarnmelder-2.pdf",
    ],
    "wartungsvertrag": [
        "few_shots/Wartungsvertrag-Wärmepumpe-1.pdf",
        "few_shots/Wartungsvertrag_für_Rauchwarnmelder-2.pdf",
    ],
}


def _sanitize_doc_name(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9 \-()\[\]]", "-", name)
    sanitized = re.sub(r" {2,}", " ", sanitized).strip("-")
    return sanitized or "document"


def _load_few_shot_blocks(doc_key: str) -> list[dict]:
    pdfs = FEW_SHOT_PDFS.get(doc_key, [])
    blocks = []
    for rel in pdfs:
        p = (BASE / rel).resolve()
        if not p.exists():
            print(f"Warning: few-shot file not found, skipping: {p}")
            continue
        blocks.append(
            {
                "document": {
                    "format": "pdf",
                    "name": _sanitize_doc_name(p.stem),
                    "source": {"bytes": p.read_bytes()},
                }
            }
        )
    return blocks


def _build_prompt(
    template: dict,
    profile: StyleProfile,
    variant_index: int,
    variant_total: int,
) -> str:
    data_section = {
        "required": template.get("required", {}),
        "optional": template.get("optional", {}),
    }
    return f"""
You are an AI system that converts structured real estate data template into HTML documents with labels.

IMPORTANT RULES:
- Output ONLY valid HTML.
- The HTML MUST be wrapped exactly like:
  <HTML> ... </HTML>
- Do NOT include explanations or markdown.
- Language MUST be German.
- Keep formatting professional and realistic.
- Keep all labels from the input data (e.g. <modell>, <typ>) in the HTML output, do not replace them with actual values.
- Labels MUST be written as HTML entities: use &lt; and &gt; instead of < and >. For example: &lt;typ&gt;, &lt;modell&gt;.

STYLE PROFILE:
Name: {profile.name}
Description: {profile.description}

Variant: {variant_index}/{variant_total}

INPUT DATA (FROM TEMPLATE SOURCE):
{json.dumps(data_section, indent=2, ensure_ascii=False)}
"""


def _extract_html(text: str) -> str:
    match = re.search(r"<HTML>(.*?)</HTML>", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match2 = re.search(r"<html.*?>.*?</html>", text, flags=re.DOTALL | re.IGNORECASE)
    if match2:
        return match2.group(0).strip()
    print("Warning: HTML wrapper not found, returning raw output")
    return text.strip()


def _call_llm(doc_blocks: list[dict], prompt_text: str) -> str:
    content = [*doc_blocks, {"text": prompt_text}]
    response = _bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": content}],
        inferenceConfig={"maxTokens": 10000},
    )
    return response["output"]["message"]["content"][0]["text"]


def generate_html(
    template: dict,
    doc_key: str,
    style_key: str,
    out_stem: Path,
    doc_blocks: list[dict],
    variant_index: int,
    variant_total: int,
) -> dict:
    if style_key not in _STYLE_MAP:
        raise KeyError(f"Unknown style '{style_key}'. Options: {list(_STYLE_MAP)}")
    profile = _STYLE_MAP[style_key]

    raw_path = Path(f"{out_stem}_{style_key}.raw.txt")
    html_path = Path(f"{out_stem}_{style_key}.html")

    try:
        print(f"[{variant_index}/{variant_total}] Generating '{style_key}'...")
        prompt = _build_prompt(template, profile, variant_index, variant_total)
        raw_text = _call_llm(doc_blocks, prompt)

        raw_path.write_text(raw_text, encoding="utf-8")

        html = _extract_html(raw_text)
        html_path.write_text(html, encoding="utf-8")

        print(f"  HTML saved: {html_path}")
        return {
            "style": style_key,
            "status": "ok",
            "html": str(html_path),
            "raw": str(raw_path),
        }

    except Exception as e:
        print(f"  FAILED '{style_key}': {e}")
        return {"style": style_key, "status": "failed", "error": str(e)}


def generate_html_variants(
    template: dict,
    doc_key: str,
    style_keys: list[str],
    out_stem: Path,
    use_few_shots: bool = True,
) -> list[dict]:
    doc_blocks = _load_few_shot_blocks(doc_key) if use_few_shots else []
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    total = len(style_keys)

    results: list[dict] = [None] * total
    with ThreadPoolExecutor(max_workers=total) as executor:
        futures = {
            executor.submit(
                generate_html,
                template,
                doc_key,
                key,
                out_stem,
                doc_blocks,
                i + 1,
                total,
            ): i
            for i, key in enumerate(style_keys)
        }
        for future in as_completed(futures):
            results[futures[future]] = future.result()

    return results


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit(
            "Usage: python3 html_generator.py <template_json> <doc_key> [<style_key|all>] [--no-few-shots]"
        )

    template_path = Path(args[0])
    if not template_path.exists():
        raise SystemExit(f"Template file not found: {template_path}")

    doc_key = args[1]
    positional = [a for a in args[2:] if not a.startswith("--")]
    style_arg = positional[0] if positional else "all"
    use_few_shots = "--no-few-shots" not in args

    style_keys = list(_STYLE_MAP.keys()) if style_arg == "all" else [style_arg]

    template = json.loads(template_path.read_text(encoding="utf-8"))
    out_stem = BASE / "output" / "html" / template_path.stem

    results = generate_html_variants(
        template, doc_key, style_keys, out_stem, use_few_shots
    )

    print("\n=== DONE ===")
    print(json.dumps(results, indent=2, ensure_ascii=False))
