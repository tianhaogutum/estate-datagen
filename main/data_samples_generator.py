"""
Data Sample Generator

Reads one or more template JSONs and a scenario specification, then asks the
LLM to fill every placeholder with realistic fabricated values.  All templates
are filled in a SINGLE LLM call so that values are consistent across documents
(e.g. the same building address appears in both the contract and the protocol).

Usage:
    python3 data_sample_generator.py \\
        --template <template1.json> [--template <template2.json> ...] \\
        --scenario <scenario_spec.txt> \\
        [--out-dir <dir>]          (default: output/data/<scenario_stem>/)

    Each template produces one output file:
        <out_dir>/<template_stem>.json

Legacy single-template usage (backward-compatible):
    python3 data_sample_generator.py <template_json> <scenario_spec> [<out_json>]
"""

from __future__ import annotations

import json
import platform
import re
import sys
from pathlib import Path

import boto3

BASE = Path(__file__).parent

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"

if platform.system() == "Windows":
    _session = boto3.Session(profile_name="claude-bedrock", region_name=BEDROCK_REGION)
    _bedrock_client = _session.client("bedrock-runtime")
else:
    _bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)


# ── Prompt ────────────────────────────────────────────────────────────────────


def _make_keys(templates: list[dict]) -> list[str]:
    """Return a unique key per template; append _1/_2/… when the entity repeats."""
    counts: dict[str, int] = {}
    for t in templates:
        e = t.get("meta", {}).get("entity", "Document")
        counts[e] = counts.get(e, 0) + 1
    seen: dict[str, int] = {}
    keys = []
    for t in templates:
        e = t.get("meta", {}).get("entity", "Document")
        if counts[e] > 1:
            seen[e] = seen.get(e, 0) + 1
            keys.append(f"{e}_{seen[e]}")
        else:
            keys.append(e)
    return keys


def _build_prompt(templates: list[dict], scenario_text: str) -> str:
    keys = _make_keys(templates)
    sections = []
    for key, t in zip(keys, templates):
        data_section = {
            "required": t.get("required", {}),
            "optional": t.get("optional", {}),
        }
        sections.append(
            f'  "{key}": {json.dumps(data_section, indent=4, ensure_ascii=False)}'
        )

    combined = "{\n" + ",\n".join(sections) + "\n}"

    return f"""
You are a data generator for German real estate maintenance documents.

You are given a set of JSON templates (one per document type) where every value
is a placeholder like "<Typ>" or "<Datum_1>".
Your task is to replace EVERY placeholder with a realistic, fabricated (but
plausible) German value.

IMPORTANT: All documents belong to the SAME scenario — values that should match
across documents MUST be consistent (same building address, same device_type,
same service provider, overlapping dates where appropriate).

RULES:
- Output ONLY valid JSON. No explanation, no markdown fences.
- The output must have one top-level key per entity, exactly matching the input keys.
- Each entity value must have exactly "required" and "optional" keys.
- Preserve the exact structure (keys, nesting, array lengths) from each template.
- Replace every "<...>" placeholder with a real value appropriate for that field.
- Dates must be ISO format YYYY-MM-DD.
- Monetary values must be numbers, not strings.
- All text values must be in German.
- Do NOT add or remove any keys compared to the templates.
- Apply the scenario instructions below when generating values.

SCENARIO INSTRUCTIONS:
---
{scenario_text}
---

TEMPLATES TO FILL:
{combined}
"""


# ── JSON parsing ──────────────────────────────────────────────────────────────


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


# ── Meta derivation ───────────────────────────────────────────────────────────


def _derive_meta_values(meta_schema: dict, filled: dict) -> dict:
    all_data = {**filled.get("required", {}), **filled.get("optional", {})}

    def _get(*path):
        node = all_data
        for key in path:
            if not isinstance(node, dict):
                return None
            node = node.get(key)
        return node

    def _first_list_item(*path):
        node = all_data
        for key in path:
            if not isinstance(node, dict):
                return None
            node = node.get(key)
        if isinstance(node, list) and node:
            item = node[0]
            return item.get("Datum") if isinstance(item, dict) else item
        return None

    FIELD_RESOLVERS: dict = {
        "device_type": lambda: _get("Anlagentyp", "Typ"),
        "contract_date": lambda: _first_list_item("Unterschriften"),
        "contract_start": lambda: _get("Laufzeit", "Startdatum"),
        "contract_end": lambda: _get("Laufzeit", "Enddatum"),
        "maintenance_frequency": lambda: _get("Wartungsintervall"),
        "cost_per_maintenance": lambda: _get("Kosten", "Betrag"),
        "termination_period_months": lambda: _get(
            "Laufzeit", "Kuendigungsfrist", "Frist"
        ),
        "maintenance_date": lambda: _get("Datum_der_Wartung"),
        "maintenance_type": lambda: _get("Wartungstyp"),
        "result_deficiency": lambda: _get("Wartungsergebnis"),
    }

    result = {"entity": meta_schema.get("entity"), "field_values": {}}
    for field in meta_schema.get("fields", []):
        name = field["name"]
        resolver = FIELD_RESOLVERS.get(name)
        result["field_values"][name] = resolver() if resolver else None

    return result


# ── Core generation ───────────────────────────────────────────────────────────


def generate_data_multi(
    templates: list[dict],
    scenario_spec_path: Path,
) -> list[dict]:
    """Fill multiple templates in one LLM call. Returns one result per template."""
    if not scenario_spec_path.exists():
        raise FileNotFoundError(f"Scenario spec not found: {scenario_spec_path}")
    scenario_text = scenario_spec_path.read_text(encoding="utf-8").strip()

    prompt = _build_prompt(templates, scenario_text)
    response = _bedrock_client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 8000},
    )
    raw = response["output"]["message"]["content"][0]["text"]
    combined = _extract_json(raw)

    keys = _make_keys(templates)
    results = []
    for key, template in zip(keys, templates):
        filled = combined.get(key)
        if filled is None:
            raise ValueError(f"LLM response missing key '{key}'. Got: {list(combined)}")
        if "required" not in filled or "optional" not in filled:
            raise ValueError(f"Key '{key}' missing 'required'/'optional' keys")

        meta_values = _derive_meta_values(template.get("meta", {}), filled)
        results.append(
            {
                "meta": meta_values,
                "required": filled["required"],
                "optional": filled["optional"],
            }
        )

    return results


def generate_data(template: dict, scenario_spec_path: Path) -> dict:
    """Single-template convenience wrapper."""
    return generate_data_multi([template], scenario_spec_path)[0]


def generate_data_to_dir(
    templates: list[dict],
    template_paths: list[Path],
    scenario_spec_path: Path,
    out_dir: Path,
) -> list[Path]:
    results = generate_data_multi(templates, scenario_spec_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    keys = _make_keys(templates)
    out_paths = []
    for key, result, tpath in zip(keys, results, template_paths):
        out_path = out_dir / f"{key}.json"
        out_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"  Saved: {out_path}")
        out_paths.append(out_path)
    return out_paths


def generate_data_to_file(
    template: dict, scenario_spec_path: Path, out_path: Path
) -> dict:
    result = generate_data(template, scenario_spec_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Data saved to: {out_path}")
    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    # ── new multi-template flag syntax ────────────────────────────────────────
    if "--template" in args or "--scenario" in args:
        template_paths: list[Path] = []
        scenario_path: Path | None = None
        out_dir: Path | None = None

        i = 0
        while i < len(args):
            if args[i] == "--template" and i + 1 < len(args):
                template_paths.append(Path(args[i + 1]))
                i += 2
            elif args[i] == "--scenario" and i + 1 < len(args):
                scenario_path = Path(args[i + 1])
                i += 2
            elif args[i] == "--out-dir" and i + 1 < len(args):
                out_dir = Path(args[i + 1])
                i += 2
            else:
                i += 1

        if not template_paths:
            raise SystemExit("Provide at least one --template <path>")
        if scenario_path is None:
            raise SystemExit("Provide --scenario <path>")

        for p in template_paths:
            if not p.exists():
                raise SystemExit(f"Template not found: {p}")

        if out_dir is None:
            out_dir = BASE / "output" / "data" / scenario_path.stem

        templates = [json.loads(p.read_text(encoding="utf-8")) for p in template_paths]
        print(
            f"Generating {len(templates)} document(s) for scenario '{scenario_path.stem}'..."
        )
        generate_data_to_dir(templates, template_paths, scenario_path, out_dir)
        print(f"Done — output in: {out_dir}")

    # ── legacy positional syntax ──────────────────────────────────────────────
    else:
        if len(args) < 2:
            raise SystemExit(
                "Usage (multi):  python3 data_sample_generator.py "
                "--template <t1.json> [--template <t2.json>] "
                "--scenario <spec.txt> [--out-dir <dir>]\n"
                "Usage (single): python3 data_sample_generator.py "
                "<template_json> <scenario_spec> [<out_json>]"
            )
        template_path = Path(args[0])
        if not template_path.exists():
            raise SystemExit(f"Template file not found: {template_path}")
        scenario_path = Path(args[1])
        template = json.loads(template_path.read_text(encoding="utf-8"))

        if len(args) >= 3:
            out_path = Path(args[2])
        else:
            stem = f"{template_path.stem}_{scenario_path.stem}"
            out_path = BASE / "output" / "data" / f"{stem}.json"

        generate_data_to_file(template, scenario_path, out_path)
