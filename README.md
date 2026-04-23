# Synthetic Data Generation — 1000plus

Generates synthetic German maintenance documents (Wartungsverträge, Wartungsprotokolle) using Claude via AWS Bedrock. The pipeline takes per-system requirement specs as input and produces diverse, high-fidelity HTML and PDF outputs across multiple visual style variants. A separate scenario layer allows post-hoc injection of domain anomalies (date mismatches, device-type inconsistencies, address errors, etc.) into generated data.

## Project Structure

```
SyntheticDataGeneration/
├── main/
│   ├── pipeline.py                    # Entry point — orchestrates the full pipeline
│   ├── data_synthesizer.py            # LLM-based JSON data generation
│   ├── doc_generator.py               # HTML template generation (few-shot prompted)
│   ├── pdf_converter.py               # HTML → PDF via Playwright (headless Chromium)
│   ├── fill_template.py               # Standalone HTML placeholder fill tool
│   ├── apply_scenarios.py             # Apply a scenario to an existing JSON data file
│   ├── taxonomy.py                    # Document types and system types
│   ├── style_profiles.py              # Visual style variants
│   ├── document_requirements/         # Per-system requirement specs
│   │   ├── wartungsvertrag/           #   e.g. WAERMEPUMPE.txt, RAUCHMELDER.txt, ...
│   │   └── wartungsprotokoll/
│   ├── few_shots/                     # Example PDFs for few-shot prompting
│   ├── scenarios/                     # Scenario prompt files (one .txt per scenario)
│   ├── output/                        # Generated documents (timestamped runs, gitignored)
│   ├── output_data/                   # apply_scenarios.py outputs (gitignored)
│   └── test_cases_demo/               # Hand-crafted test cases with artifacts
│       ├── case1_protocol/            # Base Wartungsprotokoll (Blitzschutz)
│       ├── case1_vertrag/             # Base Wartungsvertrag (Blitzschutz)
│       ├── case2/                     # Multiple contracts, one physical device
│       ├── case3/                     # Protocol date outside active contract period
│       ├── case4/                     # Two protocols in same quarter (freq mismatch)
│       └── case5/                     # Protocol addresses don't match building
├── ontology_ignore/                   # OWL ontology + SHACL shapes (standalone, not wired to pipeline)
├── bk/                                # Prototyping / reference
├── requirements.txt
└── README.md
```

## Prerequisites

- Python >= 3.10
- AWS CLI configured with a profile that has Bedrock access in `eu-central-1`
- Playwright Chromium (installed via `playwright install chromium`)

## Setup

### 1. Create and activate a virtual environment

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**PowerShell:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure AWS credentials

```bash
aws configure --profile claude-bedrock
aws sts get-caller-identity --profile claude-bedrock
```

On non-Windows the pipeline uses the default boto3 credential chain. To use a named profile, update `profile_name` in `data_synthesizer.py` and `doc_generator.py`.

## Running the Pipeline

```bash
cd main
python pipeline.py <doc_key> <system_key> [--no-few-shots]
```

| Flag | Effect |
|---|---|
| _(none)_ | Full pipeline with few-shot PDF examples |
| `--no-few-shots` | Skip few-shot PDFs (faster, avoids read timeouts) |

Examples:

```bash
python pipeline.py wartungsvertrag WAERMEPUMPE
python pipeline.py wartungsprotokoll RAUCHMELDER --no-few-shots
```

The pipeline runs four stages:

1. **Synthesize** — Claude generates structured JSON from the per-system requirement spec
2. **Generate** — Claude produces an HTML template (with `&lt;label&gt;` placeholders) for each style variant
3. **Fill** — placeholders are replaced with real values (no LLM)
4. **Convert** — filled HTML is rendered to PDF via Playwright

Output is written to `main/output/<doc_key>_<system_key>_<timestamp>/`.

## Applying Scenarios

Scenarios inject deliberate anomalies into an existing JSON data file without re-running the full pipeline.

```bash
cd main
python apply_scenarios.py <scenario> <path/to/*_example.json>
```

The script reads `scenarios/<scenario>.txt` as the instruction prompt, sends it together with the input JSON to Claude, and writes the modified JSON (same structure, changed values) to `main/output_data/<scenario>_<timestamp>.json`.

Then fill a template with the new data:

```bash
python fill_template.py <html_template> <json_path> [<output_path>]
```

### Available Scenarios

| Scenario file | Anomaly |
|---|---|
| `case2` | Multiple contracts for one physical device |
| `case3_protocol` | Protocol date falls outside active contract period |
| `case3_vertrag` | Contract data aligned to case3 building/device |
| `case4_contract` | Quarterly contract (case4 base) |
| `case4_protocol1/2` | Two protocols in the same quarter |
| `case5_protocol1/2` | Protocol addresses don't match the building |

Add a new scenario by creating `main/scenarios/<name>.txt` with plain-English instructions and reference data.

## Test Cases Demo

`main/test_cases_demo/` contains hand-crafted examples, one folder per case:

| Case | Scenario |
|---|---|
| `case1_protocol` / `case1_vertrag` | Clean baseline documents (Blitzschutz) |
| `case2` | Multiple contracts, one physical device |
| `case3` | Protocol date outside active contract period |
| `case4` | Two maintenance events in one quarter (frequency violation) |
| `case5` | Protocol addresses don't match the building |

Each case folder contains an `artifacts/` subfolder with the generated JSON, HTML and PDF files.

## Supported Document Types

| doc_key | Description |
|---|---|
| `wartungsvertrag` | Maintenance contract |
| `wartungsprotokoll` | Maintenance protocol |

## Supported System Types (`system_key`)

`KLIMAANLAGE`, `WAERMEPUMPE`, `HEIZKESSEL`, `LUEFTUNGSANLAGE`, `BRANDMELDEANLAGE`, `SPRINKLER`, `RAUCHMELDER`, `FEUERSCHUTZTUER`, `RAUCHSCHUTZ_RWA`, `SICHERHEITSBELEUCHTUNG`, `AUFZUG_PERSONEN`, `ELEKTRISCHE_ANLAGE`, `HEBEANLAGE_ABWASSER`, `NOTSTROMAGGREGAT`, `FEUERSCHUTZABSCHLUSS`, `FEUERSCHUTZEINRICHTUNG_MANUELL`, `SANITAER_ALLG`, `ELEKTRISCHE_ANLAGE_MOBIL`, `BLITZSCHUTZ`, `DRUCKBEHAELTER`, `CO_WARNANLAGE`

Each `(doc_key, system_key)` pair requires a matching spec at `main/document_requirements/<doc_key>/<system_key>.txt`.

## Tech Stack

- **Claude Sonnet 4.6** via AWS Bedrock (`eu.anthropic.claude-sonnet-4-6`, `eu-central-1`)
- **Playwright / Chromium** for HTML-to-PDF rendering
- **boto3** for AWS authentication
