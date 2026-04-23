"""Run SHACL validation against one or more RDF data files.

Usage:
    python scripts/validate.py examples/valid.ttl
    python scripts/validate.py examples/*.ttl
"""

from __future__ import annotations

import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_TTL = ROOT / "schema" / "wartung.ttl"
SHAPES_TTL = ROOT / "schema" / "shapes.ttl"


def validate_file(data_path: Path) -> tuple[bool, str]:
    data_graph = Graph().parse(data_path, format="turtle")
    shapes_graph = Graph().parse(SHAPES_TTL, format="turtle")
    ontology_graph = Graph().parse(ONTOLOGY_TTL, format="turtle")

    conforms, _results_graph, report_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        ont_graph=ontology_graph,
        inference="rdfs",
        advanced=True,
        meta_shacl=False,
        debug=False,
    )
    return conforms, report_text


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2

    overall_ok = True
    for arg in argv:
        path = Path(arg)
        if not path.exists():
            print(f"!! {path}: file not found")
            overall_ok = False
            continue

        conforms, report = validate_file(path)
        banner = "OK" if conforms else "VIOLATION"
        print(f"\n=== {path.name} — {banner} ===")
        print(report.strip())
        if not conforms:
            overall_ok = False

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
