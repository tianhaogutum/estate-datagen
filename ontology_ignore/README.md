# Wartungs- & Prüfmanagement — Ontology + SHACL

Independent semantic layer for the maintenance domain described in
`Wartungs- & Prüfmanagement — Ontology (Compact).pdf`. This module is
self-contained and is **not wired into `main/pipeline.py`** — it exists so
that RDF data can be validated against the domain rules on its own.

## Layout

```
ontology/
├── schema/
│   ├── wartung.ttl        # OWL ontology: classes, properties, SKOS device_type vocab
│   └── shapes.ttl         # SHACL shapes: field constraints + 4 coherence rules
├── examples/
│   ├── valid.ttl
│   ├── invalid_device_type.ttl     # violates Rule 1
│   ├── invalid_protocol_dates.ttl  # violates Rule 2
│   └── invalid_overlap.ttl         # violates Rule 4
├── scripts/
│   └── validate.py        # pyshacl runner
└── requirements.txt
```

## What's modelled

### Classes
`EconomicUnit`, `Building`, `Device`, `ServiceProvider`,
`MaintenanceContract`, `MaintenanceProtocol`.

### Controlled vocabulary
`device_type` values are SKOS concepts under `:DeviceTypeScheme`
(`WAERMEPUMPE`, `HEIZKESSEL`, `RAUCHMELDER`, `SPRINKLER`, `AUFZUG`,
`KLIMAANLAGE`, `ELEKTRISCH_ALLG`). Shapes currently validate the raw
notation strings via `sh:in`.

### Coherence rules (SPARQL constraints)

| # | Rule | Severity |
|---|---|---|
| 1 | `device_type` identical across Device, Contract, Protocol | Violation |
| 2a | Protocol `maintenance_date` within `[contract_start, contract_end]` | Violation |
| 2b | Protocol dates align with `contract_start + k × interval` (±14 d) | Violation |
| 3 | `Protocol.performed_by` matches `Contract.service_provider` (substitution allowed) | Warning |
| 4 | No overlapping active contracts for same (building, device_type) | Warning |

Field-level constraints (datatypes, required cardinalities, enums, date
ordering `contract_start ≥ contract_date`, etc.) are separate
`sh:property` shapes on each class.

## Setup

From the repo root:

```bash
source venv/bin/activate        # reuse project venv
pip install -r ontology/requirements.txt
```

## Run

```bash
cd ontology
python scripts/validate.py examples/valid.ttl
python scripts/validate.py examples/invalid_device_type.ttl \
                           examples/invalid_protocol_dates.ttl \
                           examples/invalid_overlap.ttl
```

Exit code is `0` if every file conforms, `1` otherwise.

## Adding new test data

Write Turtle using the `https://example.org/wartung#` namespace — see
`examples/valid.ttl` for a full, conforming minimal graph. Creation
order, as per the ontology PDF:

1. `EconomicUnit`
2. `Building` (→ EconomicUnit)
3. `ServiceProvider`
4. `Device` (→ Building, set `deviceType`)
5. `MaintenanceContract` (→ Building + ServiceProvider, matching `deviceType`)
6. `MaintenanceProtocol` (→ Contract + Device, date derived from schedule)
