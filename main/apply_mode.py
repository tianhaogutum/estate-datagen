"""
Apply a scenario mode to an existing JSON data file.

Usage:
    python apply_mode.py <mode> <json_path>

    mode:       name of a file in main/modes/<mode>.txt
    json_path:  path to a *_example.json produced by the pipeline

Output:
    main/output_data/<mode>_<timestamp>.json
    Same structure as the input JSON, values modified per the scenario.
"""

from __future__ import annotations

import json
import platform
import re
import sys
from datetime import datetime
from pathlib import Path

import boto3

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"

if platform.system() == "Windows":
    _session = boto3.Session(profile_name="claude-bedrock", region_name=BEDROCK_REGION)
    _bedrock_client = _session.client("bedrock-runtime")
else:
    _bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)


BASE = Path(__file__).parent


def _read_mode(mode: str) -> str:
    path = BASE / "modes" / f"{mode}.txt"
    if not path.exists():
        available = sorted(p.stem for p in (BASE / "modes").glob("*.txt"))
        raise SystemExit(f"Unknown mode '{mode}'. Available: {available}")
    return path.read_text(encoding="utf-8")


def _build_prompt(mode_text: str, data: dict) -> str:
    return f"""You are a data editor for real estate documents.

You will receive a JSON object and a set of scenario instructions.
Your task is to modify the JSON values so they reflect the scenario.

RULES:
- Output ONLY valid JSON. No explanation, no markdown.
- The output structure must be IDENTICAL to the input (same keys, same nesting, same arrays).
- Only change the values — never add, remove, or rename keys.
- Preserve all data types (strings stay strings, numbers stay numbers, booleans stay booleans).
- Dates must remain ISO format YYYY-MM-DD.

SCENARIO INSTRUCTIONS:
Change the input JSON so it aligns with the following reference data.
For any fields not mentioned in the reference data, change them arbitrarily but keep them plausible.
---
{mode_text.strip()}
---

INPUT JSON:
---
{json.dumps(data, indent=2, ensure_ascii=False)}
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
        raise ValueError(f"No JSON object found in response:\n{text[:300]}")
    return json.loads(text[start : end + 1])


def apply_mode(mode: str, json_path: Path) -> Path:
    mode_text = _read_mode(mode)
    data = json.loads(json_path.read_text(encoding="utf-8"))

    prompt = _build_prompt(mode_text, data)

    response = _bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 3000},
    )

    raw = response["output"]["message"]["content"][0]["text"]
    result = _extract_json(raw)

    out_dir = BASE / "output_data"
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{mode}_{timestamp}.json"
    out_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Output saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python apply_mode.py <mode> <json_path>")
    apply_mode(sys.argv[1], Path(sys.argv[2]))
