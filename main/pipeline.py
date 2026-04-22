"""
End-to-end pipeline:
    requirements.txt  ->  [Synthesizer LLM]  ->  JSON data
    JSON data + few-shots  ->  [Generator LLM]  ->  HTML  ->  PDF

Usage:
    python3 pipeline.py <doc_key>
where <doc_key> is one of: wartungsvertrag, wartungsprotokoll
"""

import sys
from datetime import datetime
from pathlib import Path

from data_synthesizer import synthesize_to_file
from doc_generator import generate_document
from pdf_converter import convert_variants
from taxonomy import REAL_ESTATE_TAXONOMY


def run(doc_key: str) -> None:
    if doc_key not in REAL_ESTATE_TAXONOMY:
        raise SystemExit(
            f"Unknown doc_key '{doc_key}'. Options: {list(REAL_ESTATE_TAXONOMY)}"
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(__file__).parent / "output" / f"{doc_key}_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    data_path = out_dir / f"{doc_key}_data.json"

    print(f"\n[1/3] Synthesizing data for '{doc_key}'...")
    data = synthesize_to_file(doc_key, data_path)

    print(f"\n[2/3] Generating HTML variants for '{doc_key}'...")
    stem = out_dir / f"{doc_key}_rendered"
    artifacts = generate_document(doc_key, data, stem)

    print(f"\n[3/3] Converting HTML to PDF...")
    convert_variants(artifacts["variants"])

    print("\nDone.")
    print(f"  run dir: {out_dir}")
    print(f"  data:    {data_path}")
    for v in artifacts["variants"]:
        if v["status"] == "ok":
            print(f"  [{v['profile']}] html: {v['html']}")
            if "pdf" in v:
                print(f"  [{v['profile']}] pdf:  {v['pdf']}")
            if "pdf_error" in v:
                print(f"  [{v['profile']}] pdf FAILED: {v['pdf_error']}")
        else:
            print(f"  [{v['profile']}] FAILED: {v.get('error', '?')}")


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "wartungsvertrag"
    run(key)
