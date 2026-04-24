"""
Fill an HTML template with values from a JSON data file.

Usage:
    python fill_template.py <html_template> <json_path> [<output_path>]

    html_template:  path to an HTML file containing &lt;label&gt; placeholders
    json_path:      path to a JSON file (must have "required" / "optional" keys,
                    or be a flat dict — both are handled)
    output_path:    optional; defaults to <html_template stem>_filled.html

Example:
    python fill_template.py \\
        test_cases_demo/case1/wartungsvertrag_rendered_01_corporate_formal.html \\
        test_cases_demo/case2/case2_20260423_155020.json
"""

from __future__ import annotations

import json
import sys
import uuid
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
    # Support both {"required": {...}, "optional": {...}} and flat dicts
    if "required" in data or "optional" in data:
        flat: dict[str, str] = {}
        for section in ("required", "optional"):
            flat.update(_flatten(data.get(section, {})))
    else:
        flat = _flatten(data)

    for key, value in flat.items():
        html = html.replace(f"&lt;{key}&gt;", value)
    return html


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2

    html_path = Path(argv[0])
    json_path = Path(argv[1])
    _uid = uuid.uuid4().hex[:8]
    out_path = (
        Path(argv[2])
        if len(argv) >= 3
        else html_path.with_name(html_path.stem + f"_filled_{_uid}.html")
    )

    if not html_path.exists():
        print(f"!! HTML template not found: {html_path}")
        return 1
    if not json_path.exists():
        print(f"!! JSON file not found: {json_path}")
        return 1

    html = html_path.read_text(encoding="utf-8")
    data = json.loads(json_path.read_text(encoding="utf-8"))

    filled = fill_html(html, data)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(filled, encoding="utf-8")
    print(f"Filled HTML saved to: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
