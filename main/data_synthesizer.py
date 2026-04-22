"""
Data Synthesizer

LLM-backed tool that reads a document requirements .txt file and produces a
JSON payload containing synthetic contract data.

This version outputs TWO datasets:
1. real data (fully generated values)
2. placeholder data (template-style values using <field_name>)
"""

import json
import platform
import re
from pathlib import Path

import boto3
from taxonomy import REAL_ESTATE_TAXONOMY, DocumentType

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"

if platform.system() == "Windows":
    print("Detected Windows")
    _session = boto3.Session(profile_name="claude-bedrock", region_name=BEDROCK_REGION)
    _bedrock_client = _session.client("bedrock-runtime")

else:
    print("Detected non-Windows OS, using default boto3 client")
    _bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)


def _read_requirements(doc: DocumentType) -> str:
    path = Path(__file__).parent / doc.requirements_file
    return path.read_text(encoding="utf-8")


def _build_prompt(requirements_text: str, doc_name: str) -> str:
    return f"""
You are a data generator for real estate documents.

Read the requirements below for a "{doc_name}" and produce ONE realistic
JSON object with fabricated (but plausible) data.

- When generating placeholder values:
  - NEVER reuse identical placeholders in arrays.
  - Each item in a list MUST be unique.
  - You MUST differentiate items using an index or unique suffix.
  - Example format: "<field_1>", "<field_2>", "<field_3>"
  - DO NOT output repeated identical placeholders like "<field>", "<field>", "<field>".

Rules:
- Top-level keys MUST be exactly "required" and "optional".
- "required" MUST include every field listed under REQUIRED FIELDS.
- "optional" MUST include a realistic subset (at least 2) of OPTIONAL FIELDS.
- Omit optional fields you do not use.
- Use realistic values (no placeholders like "John Doe").
- Dates must be ISO format YYYY-MM-DD.
- Monetary values must be numbers, not strings.
- Output ONLY valid JSON. No explanation, no markdown.

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
        raise ValueError(f"No JSON object found:\n{text[:300]}")

    return json.loads(text[start : end + 1])


def _to_placeholder(obj, parent_key: str = "", index: int = 0):
    """
    Convert real JSON into placeholder JSON.

    Example:
        "typ": "Heat Pump"          -> "typ": "<typ>"
        list item 2: "arbeit": ...  -> "arbeit": "<arbeit_2>"
    """

    if isinstance(obj, dict):
        return {k: _to_placeholder(v, k, index) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [
            _to_placeholder(item, parent_key, idx + 1) for idx, item in enumerate(obj)
        ]

    else:
        if parent_key:
            if index:
                return f"<{parent_key}_{index}>"
            return f"<{parent_key}>"
        return "<value>"


def _validate(data: dict, doc: DocumentType) -> None:
    if "required" not in data or "optional" not in data:
        raise ValueError("Missing top-level keys: required / optional")

    missing = [f for f in doc.required_fields if f not in data["required"]]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")


def synthesize(doc_key: str) -> dict:
    if doc_key not in REAL_ESTATE_TAXONOMY:
        raise KeyError(f"Unknown document type: {doc_key}")

    doc = REAL_ESTATE_TAXONOMY[doc_key]
    prompt = _build_prompt(_read_requirements(doc), doc.name)

    response = _bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 3000},
    )

    raw = response["output"]["message"]["content"][0]["text"]
    data = _extract_json(raw)

    _validate(data, doc)

    return {"real": data, "placeholder": _to_placeholder(data)}


def synthesize_to_file(doc_key: str, out_path: Path) -> dict:
    result = synthesize(doc_key)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    real_path = out_path.with_name(out_path.stem + "_example.json")
    template_path = out_path.with_name(out_path.stem + "_template.json")

    real_path.write_text(
        json.dumps(result["real"], indent=2, ensure_ascii=False), encoding="utf-8"
    )

    template_path.write_text(
        json.dumps(result["placeholder"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Real data saved to: {real_path}")
    print(f"Template data saved to: {template_path}")

    return result


if __name__ == "__main__":
    import sys

    doc_key = sys.argv[1] if len(sys.argv) > 1 else "purchase_agreement"
    out = Path(__file__).parent / "output" / f"{doc_key}_data.json"

    synthesize_to_file(doc_key, out)
