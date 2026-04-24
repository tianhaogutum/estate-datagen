"""
Fill HTML

Replaces &lt;label&gt; placeholders in an HTML file with real values from a
data JSON (output of data_sample_generator.py).

Usage:
    python3 fill_html.py <data_json> <template_html> [<out_html>]

    data_json     : path to filled data JSON (with required / optional keys)
    template_html : path to HTML file with &lt;Label&gt; placeholders
    out_html      : optional output path (default: <template_stem>_filled.html)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _flatten(obj, prefix: str = "", index: int = 0) -> dict[str, str]:
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


def fill_html(html: str, data: dict) -> str:
    flat = {}
    for section in ("required", "optional"):
        flat.update(_flatten(data.get(section, {})))

    for key, value in flat.items():
        html = html.replace(f"&lt;{key}&gt;", value)
    return html


def fill_html_file(
    data_path: Path, html_path: Path, out_path: Path | None = None
) -> Path:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")

    filled = fill_html(html, data)

    if out_path is None:
        out_dir = Path(__file__).parent / "output" / "filled"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / (html_path.stem + "_filled.html")

    out_path.write_text(filled, encoding="utf-8")
    print(f"Filled HTML saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit(
            "Usage: python3 fill_html.py <data_json> <template_html> [<out_html>]"
        )

    data_path = Path(args[0])
    html_path = Path(args[1])
    out_path = Path(args[2]) if len(args) >= 3 else None

    for p in (data_path, html_path):
        if not p.exists():
            raise SystemExit(f"File not found: {p}")

    fill_html_file(data_path, html_path, out_path)
