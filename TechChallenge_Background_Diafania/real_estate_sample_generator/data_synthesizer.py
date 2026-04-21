"""
Data Synthesizer

LLM-backed tool that reads a document requirements .txt file and produces a
JSON payload containing synthetic contract data. The output JSON separates
required fields (always present) from optional fields (a realistic subset).
"""

import json
import re
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from taxonomy import REAL_ESTATE_TAXONOMY, DocumentType

load_dotenv()
_client = anthropic.Anthropic()

SYNTHESIZER_MODEL = "claude-sonnet-4-20250514"


def _read_requirements(doc: DocumentType) -> str:
    path = Path(__file__).parent / doc.requirements_file
    return path.read_text(encoding="utf-8")


def _build_prompt(requirements_text: str, doc_name: str) -> str:
    return f"""You are a data generator for real estate documents.

Read the requirements below for a "{doc_name}" and produce ONE realistic
JSON object with fabricated (but plausible) data.

Rules:
- Top-level keys MUST be exactly "required" and "optional".
- "required" MUST include every field listed under REQUIRED FIELDS.
- "optional" MUST include a realistic subset (at least 2) of the OPTIONAL FIELDS.
  Omit optional keys you choose not to fill rather than leaving them empty.
- Use varied, realistic values — not placeholders like "John Doe" or "123 Main St".
- Dates in ISO format YYYY-MM-DD. Monetary amounts as numbers, not strings.
- Output ONLY the JSON object. No prose, no code fences.

REQUIREMENTS:
---
{requirements_text}
---
"""


def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in model output:\n{text[:300]}")
    return json.loads(text[start : end + 1])


def synthesize(doc_key: str) -> dict:
    if doc_key not in REAL_ESTATE_TAXONOMY:
        raise KeyError(f"Unknown document type: {doc_key}")
    doc = REAL_ESTATE_TAXONOMY[doc_key]
    prompt = _build_prompt(_read_requirements(doc), doc.name)

    with _client.messages.stream(
        model=SYNTHESIZER_MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()

    raw = msg.content[0].text
    data = _extract_json(raw)
    _validate(data, doc)
    return data


def _validate(data: dict, doc: DocumentType) -> None:
    if "required" not in data or "optional" not in data:
        raise ValueError("Output missing 'required' or 'optional' top-level keys.")
    missing = [f for f in doc.required_fields if f not in data["required"]]
    if missing:
        raise ValueError(f"Missing required fields in synthesized data: {missing}")


def synthesize_to_file(doc_key: str, out_path: Path) -> dict:
    data = synthesize(doc_key)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Synthesized data saved to {out_path}")
    return data


if __name__ == "__main__":
    import sys

    doc_key = sys.argv[1] if len(sys.argv) > 1 else "purchase_agreement"
    out = Path(__file__).parent / "output" / f"{doc_key}_data.json"
    synthesize_to_file(doc_key, out)
