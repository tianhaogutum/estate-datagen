"""
End-to-end pipeline:
    requirements.txt  ->  [Synthesizer LLM]  ->  JSON data
    JSON data + few-shots  ->  [Generator LLM]  ->  HTML

Usage:
    python3 pipeline.py <doc_key> <system_key>

    doc_key:    wartungsvertrag | wartungsprotokoll
    system_key: KLIMAANLAGE | WAERMEPUMPE | HEIZKESSEL | LUEFTUNGSANLAGE |
                BRANDMELDEANLAGE | SPRINKLER | RAUCHMELDER | FEUERSCHUTZTUER |
                RAUCHSCHUTZ_RWA | SICHERHEITSBELEUCHTUNG | AUFZUG_PERSONEN |
                ELEKTRISCHE_ANLAGE | HEBEANLAGE_ABWASSER | NOTSTROMAGGREGAT
"""

import sys
from datetime import datetime
from pathlib import Path

from data_synthesizer import synthesize_to_file
from doc_generator import generate_document
from pdf_converter import convert_html_to_pdf
from taxonomy import REAL_ESTATE_TAXONOMY, SYSTEM_TYPES


def _flatten(obj, prefix: str = "", index: int = 0) -> dict[str, str]:
    """Recursively flatten a JSON object into {label: value} pairs matching _to_placeholder format."""
    result = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            result.update(_flatten(v, k, index))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj, start=1):
            result.update(_flatten(item, prefix, idx))
    else:
        key = f"{prefix}_{index}" if index else prefix
        result[key] = (
            str(obj) if not isinstance(obj, bool) else ("ja" if obj else "nein")
        )
    return result


def fill_html(html: str, real_data: dict) -> str:
    """Replace &lt;label&gt; placeholders in HTML with real values."""
    flat = {}
    for section in ("required", "optional"):
        flat.update(_flatten(real_data.get(section, {})))

    for key, value in flat.items():
        html = html.replace(f"&lt;{key}&gt;", value)
    return html


def run(doc_key: str, system_key: str) -> None:
    if doc_key not in REAL_ESTATE_TAXONOMY:
        raise SystemExit(
            f"Unknown doc_key '{doc_key}'. Options: {list(REAL_ESTATE_TAXONOMY)}"
        )
    if system_key not in SYSTEM_TYPES:
        raise SystemExit(
            f"Unknown system_key '{system_key}'. Options: {list(SYSTEM_TYPES)}"
        )

    base = Path(__file__).parent
    doc = REAL_ESTATE_TAXONOMY[doc_key]

    req_file = base / doc.requirements_file_for(system_key)
    if not req_file.exists():
        raise SystemExit(f"Requirements file not found: {req_file}")

    for pdf in doc.few_shot_files:
        pdf_path = base / pdf
        if not pdf_path.exists():
            raise SystemExit(f"Few-shot file not found: {pdf_path}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(__file__).parent / "output" / f"{doc_key}_{system_key}_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    data_path = out_dir / f"{doc_key}_data.json"

    print(f"\n[1/4] Synthesizing data for '{doc_key}' / '{system_key}'...")
    data = synthesize_to_file(doc_key, data_path, system_key)

    print(f"\n[2/4] Generating HTML variants for '{doc_key}'...")
    stem = out_dir / f"{doc_key}_rendered"
    artifacts = generate_document(doc_key, data, stem)

    print("\n[3/4] Filling HTML placeholders with real data...")
    for v in artifacts["variants"]:
        if v["status"] != "ok":
            continue
        html_path = Path(v["html"])
        filled_html = fill_html(html_path.read_text(encoding="utf-8"), data["real"])
        filled_path = html_path.with_name(html_path.stem + "_filled.html")
        filled_path.write_text(filled_html, encoding="utf-8")
        v["html_filled"] = str(filled_path)

    print("\n[4/4] Converting filled HTML to PDF...")
    for v in artifacts["variants"]:
        if v["status"] != "ok" or "html_filled" not in v:
            continue
        try:
            pdf_path = convert_html_to_pdf(Path(v["html_filled"]))
            v["pdf"] = str(pdf_path)
        except Exception as e:
            print(f"PDF conversion failed for {v['profile']}: {e}")
            v["pdf_error"] = str(e)

    print("\nDone.")
    print(f"  run dir: {out_dir}")
    print(f"  data:    {data_path}")
    for v in artifacts["variants"]:
        if v["status"] == "ok":
            print(f"  [{v['profile']}] template: {v['html']}")
            print(f"  [{v['profile']}] filled:   {v['html_filled']}")
            if "pdf" in v:
                print(f"  [{v['profile']}] pdf:  {v['pdf']}")
            if "pdf_error" in v:
                print(f"  [{v['profile']}] pdf FAILED: {v['pdf_error']}")
        else:
            print(f"  [{v['profile']}] FAILED: {v.get('error', '?')}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python3 pipeline.py <doc_key> <system_key>")
    run(sys.argv[1], sys.argv[2])
