"""
Document Generator

LLM-backed tool that consumes (a) synthesized JSON contract data and
(b) real PDF few-shot examples (sent as base64 document blocks), then
produces an HTML rendering of the document.
Renders the HTML to PDF.
"""

import base64
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import boto3
from weasyprint import HTML

from style_profiles import StyleProfile, get_profiles
from taxonomy import REAL_ESTATE_TAXONOMY, DocumentType

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"

_bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)


def _pdf_base64(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("utf-8")


def _few_shot_document_blocks(doc: DocumentType) -> list[dict]:
    base = Path(__file__).parent
    blocks = []
    for rel in doc.few_shot_files:
        p = (base / rel).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Few-shot file not found: {p}")
        blocks.append(
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": _pdf_base64(p),
                },
            }
        )
    return blocks


def _build_prompt_text(
    data: dict,
    doc_name: str,
    n_shots: int,
    profile: StyleProfile,
    variant_index: int,
    variant_total: int,
) -> str:
    return f"""You are an AI that renders real estate documents as HTML.

GOAL: simulate the diversity of real-world German "{doc_name}" templates.
Different companies and institutions use very different layouts, fonts,
structures, and branding — we are generating {variant_total} heterogeneous
variants of the SAME underlying data to cover this real-world variety.

This is variant {variant_index}/{variant_total}. You MUST follow the assigned
STYLE PROFILE strictly and produce a layout that is visually and structurally
DISTINCT from the few-shot PDFs and from any generic default rendering.

STYLE PROFILE — {profile.name}:
{profile.description}

You are given:
1. {n_shots} FEW-SHOT PDF examples (attached above) showing the typical content
   of a German "{doc_name}". Use them only to understand terminology and the
   kinds of fields/sections that appear — NOT as a visual template to copy.
2. A JSON payload with the data for the NEW document (required + optional fields).

Produce ONE complete, self-contained HTML document that renders the data.

Rules:
- Language: GERMAN.
- Use EVERY field under "required" in the JSON. Surface every field present
  under "optional".
- STRICTLY follow the STYLE PROFILE above. Do NOT imitate the few-shot PDFs'
  layout, fonts, or visual style — those are content references only.
- Each of the {variant_total} variants must look clearly different from the others
  (different fonts, section ordering, table vs. list layouts, header styles,
  color accents, spacing).
- Embed CSS in a <style> tag. A4 page size (@page {{ size: A4; }}).
- Print-ready, white background (or subtle profile-appropriate accents).
- Wrap the final document EXACTLY as: <HTML>...</HTML>
- Output ONLY the wrapped HTML, nothing else.

--- DATA FOR NEW DOCUMENT ---
{json.dumps(data, indent=2, ensure_ascii=False)}
"""


def _extract_html(text: str) -> str:
    match = re.search(r"<HTML>(.*?)</HTML>", text, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError("No <HTML>...</HTML> wrapper found in model output.")
    return match.group(1).strip()


def _generate_html_for_profile(
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

    pdf_data_text = ""
    for block in doc_blocks:
        if block.get("type") == "document":
            pdf_b64 = block["source"]["data"]
            pdf_data_text = f"\n\n[SEED DOCUMENT BASE64]:\n{pdf_b64}\n"

    full_prompt = pdf_data_text + prompt_text

    response = _bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": full_prompt}]}],
        inferenceConfig={'maxTokens': 6000}
    )

    return _extract_html(response['output']['message']['content'][0]['text'])


def html_to_pdf(html: str, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html).write_pdf(str(pdf_path))
    print(f"PDF saved to {pdf_path}")


def generate_document(doc_key: str, data: dict, output_stem: Path) -> dict:
    doc = REAL_ESTATE_TAXONOMY[doc_key]
    doc_blocks = _few_shot_document_blocks(doc)
    profiles = get_profiles()
    total = len(profiles)

    Path(output_stem).parent.mkdir(parents=True, exist_ok=True)

    def _one(idx: int, profile: StyleProfile) -> dict:
        print(f"[{idx}/{total}] Generating HTML for style '{profile.key}'...")
        html = _generate_html_for_profile(doc, doc_blocks, data, profile, idx, total)
        html_path = Path(f"{output_stem}_{idx:02d}_{profile.key}.html")
        pdf_path = Path(f"{output_stem}_{idx:02d}_{profile.key}.pdf")
        html_path.write_text(html, encoding="utf-8")
        print(f"HTML saved to {html_path}")
        html_to_pdf(html, pdf_path)
        return {"profile": profile.key, "html": html_path, "pdf": pdf_path}

    variants: list[dict] = [None] * total
    with ThreadPoolExecutor(max_workers=total) as executor:
        futures = {
            executor.submit(_one, i + 1, profile): i
            for i, profile in enumerate(profiles)
        }
        for future in as_completed(futures):
            i = futures[future]
            variants[i] = future.result()

    return {"variants": variants}


if __name__ == "__main__":
    import sys

    doc_key = sys.argv[1] if len(sys.argv) > 1 else "wartungsvertrag"
    data_path = Path(__file__).parent / "output" / f"{doc_key}_data.json"
    if not data_path.exists():
        raise SystemExit(f"Run data_synthesizer.py first — {data_path} missing.")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    stem = Path(__file__).parent / "output" / f"{doc_key}_rendered"
    generate_document(doc_key, data, stem)
