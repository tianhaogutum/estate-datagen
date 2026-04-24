"""
Template Generator

Reads a document-requirements .txt and the matching entities-meta .json,
then asks the LLM to produce a placeholder-only template JSON (no real data).

Usage:
    python3 template_generator.py <doc_key> <system_key> [<out_path>]

    doc_key:    wartungsvertrag | wartungsprotokoll
    system_key: KLIMAANLAGE | WAERMEPUMPE | HEIZKESSEL | ...
    out_path:   optional output file (default: stdout)

Output structure:
    {
      "meta":     { ...fields from entities_meta/<doc_key>.json... },
      "required": { "<Field>": "<Field>", ... },
      "optional": { "<Field>": "<Field>", ... }
    }
"""

from __future__ import annotations

import json
import platform
import re
import sys
from pathlib import Path

import boto3

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"
BASE = Path(__file__).parent

if platform.system() == "Windows":
    _session = boto3.Session(profile_name="claude-bedrock", region_name=BEDROCK_REGION)
    _bedrock_client = _session.client("bedrock-runtime")
else:
    _bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)


def _read_requirements(doc_key: str, system_key: str) -> str:
    path = BASE / "document_requirements" / doc_key / f"{system_key}.txt"
    if not path.exists():
        raise FileNotFoundError(
            f"No requirements file for '{doc_key}' / '{system_key}': {path}"
        )
    return path.read_text(encoding="utf-8")


def _read_meta(doc_key: str) -> dict:
    path = BASE / "entities_meta" / f"{doc_key}.json"
    if not path.exists():
        raise FileNotFoundError(f"No entities_meta file found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _build_prompt(requirements_text: str) -> str:
    return f"""
You are a document-schema extractor.

Read the requirements below and produce a JSON template with placeholder values
(no real data). Placeholder format rules:
- Scalar fields:  "<FieldName>"
- Items in a list use an index suffix: "<FieldName_1>", "<FieldName_2>", ...
- Nested objects: each sub-key gets its own "<SubKey>" placeholder
- For lists of objects, repeat the object structure with indexed sub-keys,
  e.g. [{{"Rolle": "<Rolle_1>", "Datum": "<Datum_1>"}}, {{"Rolle": "<Rolle_2>", "Datum": "<Datum_2>"}}]
- Use at least 2 items for every list field
- Do NOT use real values (no names, dates, amounts)

Output a single JSON object with exactly two top-level keys:
  "required"  — one entry per REQUIRED FIELD, preserving nesting / list structure
  "optional"  — one entry per OPTIONAL FIELD, preserving nesting / list structure

Output ONLY valid JSON. No explanation, no markdown fences.

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
        raise ValueError(f"No JSON object in LLM response:\n{text[:400]}")
    return json.loads(text[start : end + 1])


def generate_template(doc_key: str, system_key: str) -> dict:
    requirements_text = _read_requirements(doc_key, system_key)
    meta = _read_meta(doc_key)

    prompt = _build_prompt(requirements_text)
    response = _bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 3000},
    )
    raw = response["output"]["message"]["content"][0]["text"]
    template = _extract_json(raw)

    if "required" not in template or "optional" not in template:
        raise ValueError("LLM output missing 'required' or 'optional' keys")

    return {
        "meta": meta,
        "required": template["required"],
        "optional": template["optional"],
    }


def generate_template_to_file(doc_key: str, system_key: str, out_path: Path) -> dict:
    result = generate_template(doc_key, system_key)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Template saved to: {out_path}")
    return result


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit(
            "Usage: python3 data_template_generator.py <doc_key> <system_key> [<out_path>]"
        )
    doc_key, system_key = args[0], args[1]
    if len(args) >= 3:
        out_path = Path(args[2])
    else:
        out_path = (
            BASE / "output" / "templates" / f"{doc_key}_{system_key}_template.json"
        )

    generate_template_to_file(doc_key, system_key, out_path)
