"""
Ontology View

Reads one or more data JSON files (output of data_sample_generator.py) and
assembles them into a structured ontology tree showing:

    EconomicUnit
    └─ Building (by address)
       └─ Device (by device_type)
          └─ MaintenanceContract
             └─ MaintenanceProtocol (count + dates)

Usage:
    python3 ontology_view.py <data_json> [<data_json> ...] [--out <out.json>]

Each input file must have a "meta" block with "entity" and "field_values".
Supported entity values: MaintenanceContract, MaintenanceProtocol.

The script auto-assigns surrogate IDs where real UUIDs are null.
"""

from __future__ import annotations

import json
import sys
import uuid
from collections import defaultdict
from pathlib import Path


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fv(data: dict) -> dict:
    return data.get("meta", {}).get("field_values", {})


def _req(data: dict) -> dict:
    return data.get("required", {})


def _opt(data: dict) -> dict:
    return data.get("optional", {})


def _get(d: dict, *keys):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d


def _short_id(val) -> str:
    if val:
        return str(val)[:8]
    return str(uuid.uuid4())[:8]


def build_ontology(files: list[Path]) -> dict:
    contracts: list[dict] = []
    protocols: list[dict] = []

    for f in files:
        data = _load(f)
        entity = data.get("meta", {}).get("entity")
        if entity == "MaintenanceContract":
            contracts.append(data)
        elif entity == "MaintenanceProtocol":
            protocols.append(data)
        else:
            print(f"Warning: unknown entity '{entity}' in {f.name}, skipping")

    # ── Build contract nodes ──────────────────────────────────────────────────
    contract_nodes: list[dict] = []
    for data in contracts:
        fv = _fv(data)
        req = _req(data)

        contract_id = _short_id(fv.get("id"))
        building_id = _short_id(fv.get("building_id"))
        address = (
            _get(req, "Objekt_der_Wartung", "Adresse")
            or _get(req, "Objekt_der_Wartung", "Gebäude_ID")
            or "Unbekannt"
        )
        auftraggeber = (
            _get(req, "Auftraggeber", "Name")
            or _get(req, "Auftraggeber")
            or "Unbekannt"
        )
        auftragnehmer = (
            _get(req, "Auftragnehmer", "Firma")
            or _get(req, "Auftragnehmer")
            or "Unbekannt"
        )

        contract_nodes.append(
            {
                "_contract_id": contract_id,
                "_building_id": building_id,
                "_building_address": address,
                "_economic_unit": auftraggeber,
                "device_type": fv.get("device_type")
                or _get(req, "Anlagentyp", "Typ")
                or "?",
                "service_provider": auftragnehmer,
                "contract_date": fv.get("contract_date"),
                "contract_start": fv.get("contract_start"),
                "contract_end": fv.get("contract_end"),
                "maintenance_frequency": fv.get("maintenance_frequency"),
                "cost_per_maintenance": fv.get("cost_per_maintenance"),
                "source_file": str(Path(files[contracts.index(data)]).name),
            }
        )

    # ── Build protocol nodes ──────────────────────────────────────────────────
    # Each protocol carries its own link key: contract_id if set, else
    # a fuzzy key built from device_type + address so it matches contracts.
    _contract_id_map = {cn["_contract_id"]: cn for cn in contract_nodes}

    def _proto_link_key(fv: dict, req: dict) -> str:
        raw_cid = fv.get("contract_id")
        if raw_cid:
            key = _short_id(raw_cid)
            if key in _contract_id_map:
                return key
        # fall back: match on device_type + address
        dtype = (
            (
                fv.get("device_type")
                or _get(req, "Anlagentyp", "Typ")
                or _get(req, "Anlagenstandort", "Anlagentyp")
                or ""
            )
            .strip()
            .lower()
        )
        address = (
            _get(req, "Anlagenstandort", "Adresse")
            or _get(req, "Anlagenstandort")
            or ""
        )
        if isinstance(address, dict):
            address = " ".join(str(v) for v in address.values())
        address = str(address).strip().lower()
        for cn in contract_nodes:
            cn_dtype = str(cn["device_type"]).strip().lower()
            cn_addr = str(cn["_building_address"]).strip().lower()
            if dtype and dtype in cn_dtype or cn_dtype in dtype:
                if address and (address in cn_addr or cn_addr in address):
                    return cn["_contract_id"]
            # looser: match on device_type alone if only one contract
            if (
                dtype
                and (dtype in cn_dtype or cn_dtype in dtype)
                and len(contract_nodes) == 1
            ):
                return cn["_contract_id"]
        # last resort: attach to first contract
        return contract_nodes[0]["_contract_id"] if contract_nodes else "__unmatched__"

    proto_by_contract: dict[str, list[dict]] = defaultdict(list)
    for data in protocols:
        fv = _fv(data)
        req = _req(data)
        link_key = _proto_link_key(fv, req)
        proto_by_contract[link_key].append(
            {
                "maintenance_date": fv.get("maintenance_date")
                or _get(req, "Datum_der_Wartung"),
                "maintenance_type": fv.get("maintenance_type"),
                "result_deficiency": fv.get("result_deficiency"),
                "deficiency_type": fv.get("deficiency_type"),
                "performed_by": _get(req, "Ausfuehrende_Fachfirma", "Firma"),
                "source_file": str(
                    Path(files[len(contracts) + protocols.index(data)]).name
                ),
            }
        )

    # ── Attach protocols to contracts ─────────────────────────────────────────
    for cn in contract_nodes:
        cid = cn["_contract_id"]
        protos = proto_by_contract.get(cid, [])
        cn["protocols"] = {
            "count": len(protos),
            "entries": sorted(protos, key=lambda p: p.get("maintenance_date") or ""),
        }

    # ── Assemble tree: EconomicUnit → Building → Device/Contract ─────────────
    eu_map: dict[str, dict] = {}
    for cn in contract_nodes:
        eu_name = cn["_economic_unit"]
        bld_addr = cn["_building_address"]

        if eu_name not in eu_map:
            eu_map[eu_name] = {"name": eu_name, "buildings": {}}

        bld_map = eu_map[eu_name]["buildings"]
        if bld_addr not in bld_map:
            bld_map[bld_addr] = {"address": bld_addr, "devices": []}

        bld_map[bld_addr]["devices"].append(
            {
                "device_type": cn["device_type"],
                "contract": {
                    "contract_id": cn["_contract_id"],
                    "service_provider": cn["service_provider"],
                    "contract_date": cn["contract_date"],
                    "contract_start": cn["contract_start"],
                    "contract_end": cn["contract_end"],
                    "maintenance_frequency": cn["maintenance_frequency"],
                    "cost_per_maintenance": cn["cost_per_maintenance"],
                    "source_file": cn["source_file"],
                    "protocols": cn["protocols"],
                },
            }
        )

    # ── Final output ──────────────────────────────────────────────────────────
    economic_units = []
    for eu in eu_map.values():
        buildings = []
        for bld in eu["buildings"].values():
            buildings.append(
                {
                    "address": bld["address"],
                    "device_count": len(bld["devices"]),
                    "devices": bld["devices"],
                }
            )
        economic_units.append(
            {
                "name": eu["name"],
                "building_count": len(buildings),
                "buildings": buildings,
            }
        )

    return {
        "summary": {
            "economic_units": len(economic_units),
            "buildings": sum(e["building_count"] for e in economic_units),
            "contracts": len(contracts),
            "protocols": len(protocols),
        },
        "economic_units": economic_units,
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(
            "Usage: python3 ontology_view.py <data_json> [<data_json> ...] [--out <out.json>]"
        )

    out_path: Path | None = None
    if "--out" in args:
        idx = args.index("--out")
        out_path = Path(args[idx + 1])
        args = args[:idx] + args[idx + 2 :]

    files = [Path(a) for a in args]
    for f in files:
        if not f.exists():
            raise SystemExit(f"File not found: {f}")

    result = build_ontology(files)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if out_path is None:
        out_path = Path(__file__).parent / "output" / "ontology" / "ontology_view.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    print(f"Ontology view saved to: {out_path}")
