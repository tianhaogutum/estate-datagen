"""
Document Generator (HTML Only, Robust)

Features:
- Always saves raw LLM output
- Never loses data even if HTML parsing fails
- Each variant is independently fault-tolerant
- No PDF generation
- Uses TEMPLATE dataset as input source
"""

import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import boto3

from style_profiles import StyleProfile, get_profiles
from taxonomy import REAL_ESTATE_TAXONOMY, DocumentType

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"

_bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)


# -------------------------
# Utils
# -------------------------

def _few_shot_document_blocks(doc: DocumentType) -> list[dict]:
    base = Path(__file__).parent
    blocks = []

    for rel in doc.few_shot_files:
        p = (base / rel).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Few-shot file not found: {p}")

        blocks.append(
            {
                "document": {
                    "format": "pdf",
                    "name": p.stem,
                    "source": {
                        "bytes": p.read_bytes(),
                    },
                }
            }
        )

    return blocks


# -------------------------
# Prompt (ALL ENGLISH)
# -------------------------

def _build_prompt_text(
    data: dict,
    doc_name: str,
    n_shots: int,
    profile: StyleProfile,
    variant_index: int,
    variant_total: int,
) -> str:
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
{json.dumps(data, indent=2, ensure_ascii=False)}
"""


# -------------------------
# HTML extraction (robust)
# -------------------------

def _extract_html(text: str) -> str:
    match = re.search(r"<HTML>(.*?)</HTML>", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    match2 = re.search(r"<html.*?>.*?</html>", text, flags=re.DOTALL | re.IGNORECASE)
    if match2:
        return match2.group(0).strip()

    print("⚠️ HTML wrapper not found, returning raw output")
    return text.strip()


# -------------------------
# LLM call (raw output preserved)
# -------------------------

def _generate_raw_output(
    doc: DocumentType,
    doc_blocks: list[dict],
    data: dict,
    profile: StyleProfile,
    variant_index: int,
    variant_total: int,
) -> str:

    prompt_text = _build_prompt_text(
        data, doc.name, len(doc_blocks), profile, variant_index, variant_total
    )

    content = [*doc_blocks, {"text": prompt_text}]

    response = _bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": content}],
        inferenceConfig={"maxTokens": 6000},
    )

    return response["output"]["message"]["content"][0]["text"]


# -------------------------
# Main (UNCHANGED SIGNATURE)
# -------------------------

def generate_document(doc_key: str, data: dict, output_stem: Path) -> dict:
    doc = REAL_ESTATE_TAXONOMY[doc_key]
    doc_blocks = _few_shot_document_blocks(doc)
    profiles = get_profiles()
    total = len(profiles)

    Path(output_stem).parent.mkdir(parents=True, exist_ok=True)

    def _one(idx: int, profile: StyleProfile) -> dict:
        print(f"[{idx}/{total}] Generating '{profile.key}'...")

        base_name = f"{output_stem}_{idx:02d}_{profile.key}"

        raw_path = Path(base_name + ".raw.txt")
        html_path = Path(base_name + ".html")

        try:
            raw_text = _generate_raw_output(
                doc, doc_blocks, data, profile, idx, total
            )

            raw_path.write_text(raw_text, encoding="utf-8")

            html = _extract_html(raw_text)
            html_path.write_text(html, encoding="utf-8")

            print(f"✅ HTML saved: {html_path}")

            return {
                "profile": profile.key,
                "status": "ok",
                "html": str(html_path),
                "raw": str(raw_path),
            }

        except Exception as e:
            print(f"❌ FAILED variant {profile.key}: {e}")

            return {
                "profile": profile.key,
                "status": "failed",
                "error": str(e),
            }

    results: list[dict] = [None] * total

    with ThreadPoolExecutor(max_workers=total) as executor:
        futures = {
            executor.submit(_one, i + 1, profile): i
            for i, profile in enumerate(profiles)
        }

        for future in as_completed(futures):
            i = futures[future]
            results[i] = future.result()

    return {"variants": results}


# -------------------------
# CLI (NOW USE TEMPLATE FILE)
# -------------------------

if __name__ == "__main__":
    import sys

    doc_key = sys.argv[1] if len(sys.argv) > 1 else "wartungsvertrag"

    base = Path(__file__).parent / "output"

    # 👇 CHANGED: now using TEMPLATE file instead of raw data
    data_path = base / f"{doc_key}_data_template.json"

    if not data_path.exists():
        raise SystemExit(f"Missing template file: {data_path}")

    data = json.loads(data_path.read_text(encoding="utf-8"))

    stem = base / f"{doc_key}_rendered"

    result = generate_document(doc_key, data, stem)

    print("\n=== DONE ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))