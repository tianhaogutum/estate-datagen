"""
End-to-end pipeline:
    requirements.txt  ->  [Synthesizer LLM]  ->  JSON data
    JSON data + few-shots  ->  [Generator LLM]  ->  HTML

Usage:
    python3 pipeline.py <doc_key> [<system_key>]

    doc_key:    wartungsvertrag | wartungsprotokoll
    system_key: KLIMAANLAGE | WAERMEPUMPE | HEIZKESSEL | ... (optional)
"""

import sys
from datetime import datetime
from pathlib import Path

from data_synthesizer import synthesize_to_file
from doc_generator import generate_document
from taxonomy import REAL_ESTATE_TAXONOMY, SYSTEM_TYPES


def run(doc_key: str, system_key: str | None = None) -> None:
    if doc_key not in REAL_ESTATE_TAXONOMY:
        raise SystemExit(
            f"Unknown doc_key '{doc_key}'. Options: {list(REAL_ESTATE_TAXONOMY)}"
        )
    if system_key and system_key not in SYSTEM_TYPES:
        raise SystemExit(
            f"Unknown system_key '{system_key}'. Options: {list(SYSTEM_TYPES)}"
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = (
        f"{doc_key}_{system_key}_{timestamp}"
        if system_key
        else f"{doc_key}_{timestamp}"
    )
    out_dir = Path(__file__).parent / "output" / run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    data_path = out_dir / f"{doc_key}_data.json"

    label = f"'{doc_key}'" + (f" / '{system_key}'" if system_key else "")
    print(f"\n[1/2] Synthesizing data for {label}...")
    data = synthesize_to_file(doc_key, data_path, system_key)

    print(f"\n[2/2] Generating HTML variants for {label}...")
    stem = out_dir / f"{doc_key}_rendered"
    artifacts = generate_document(doc_key, data, stem)

    print("\nDone.")
    print(f"  run dir: {out_dir}")
    print(f"  data:    {data_path}")
    for v in artifacts["variants"]:
        if v["status"] == "ok":
            print(f"  [{v['profile']}] html: {v['html']}")
        else:
            print(f"  [{v['profile']}] FAILED: {v.get('error', '?')}")


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "wartungsvertrag"
    sys_key = sys.argv[2] if len(sys.argv) > 2 else None
    run(key, sys_key)
