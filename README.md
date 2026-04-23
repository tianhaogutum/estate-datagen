# Synthetic Data Generation — 1000plus

Generates synthetic German maintenance documents (Wartungsverträge, Wartungsprotokolle) using Claude via AWS Bedrock. The pipeline takes per-system requirement specs as input and produces diverse, high-fidelity HTML and PDF outputs across multiple visual style variants, with content variation while preserving required baseline fields.

## Project Structure

```
SyntheticDataGeneration/
├── main/                              # Main pipeline
│   ├── pipeline.py                    # Entry point — orchestrates the full pipeline
│   ├── data_synthesizer.py            # LLM-based JSON data generation
│   ├── doc_generator.py               # HTML template generation (few-shot prompted)
│   ├── pdf_converter.py               # HTML → PDF via wkhtmltopdf/pdfkit
│   ├── taxonomy.py                    # Document types and system types
│   ├── style_profiles.py              # Visual style variants
│   ├── document_requirements/         # Per-system requirement specs
│   │   ├── wartungsvertrag/           #   e.g. WAERMEPUMPE.txt, RAUCHMELDER.txt, ...
│   │   └── wartungsprotokoll/
│   ├── few_shots/                     # Example PDFs for few-shot prompting
│   └── output/                        # Generated documents (timestamped runs)
├── bk/                                # Prototyping / reference
│   ├── main.py                        # Single document generation
│   ├── KONZEPT.md                     # Concept documentation
│   ├── utils/render.py                # HTML extraction & PDF (WeasyPrint)
│   └── Daten_AI_Engineer_CaseStudy/   # Seed documents (PDF, DOCX)
├── requirements.txt
├── wkhtmltopdf.pkg                    # macOS installer for wkhtmltopdf
└── README.md
```

## Prerequisites

- Python >= 3.10
- AWS CLI configured with a profile that has Bedrock access in `eu-central-1` (default profile name: `claude-bedrock`)
- **wkhtmltopdf** installed and on `PATH` (used by `pdfkit` for PDF conversion)
  - macOS: install via the bundled `wkhtmltopdf.pkg`, or `brew install --cask wkhtmltopdf`
  - Linux/Windows: see [wkhtmltopdf.org/downloads](https://wkhtmltopdf.org/downloads.html)

## Setup

### 1. Create and activate a virtual environment

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**PowerShell** (run once if needed):
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
python -m venv venv
.\venv\Scripts\activate
```

**Git Bash:**
```bash
python -m venv venv
source venv/Scripts/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure AWS credentials

The pipeline uses the AWS profile `claude-bedrock` by default. Configure it:

```bash
aws configure --profile claude-bedrock
aws sts get-caller-identity --profile claude-bedrock
```

To use a different profile, update the `profile_name` in `data_synthesizer.py` and `doc_generator.py`.

## Running the Pipeline

From the repository root:

```bash
cd main
python pipeline.py <doc_key> <system_key>
```

Example:

```bash
python pipeline.py wartungsvertrag WAERMEPUMPE
python pipeline.py wartungsprotokoll RAUCHMELDER
```

The pipeline runs four stages:

1. **Synthesize** — Claude generates structured JSON data from the matching per-system requirement spec
2. **Generate** — Claude produces an HTML template (with `&lt;label&gt;` placeholders) for each style variant, using few-shot PDF examples
3. **Fill** — placeholders are replaced with real values from the JSON (no LLM)
4. **Convert** — filled HTML is rendered to PDF via `wkhtmltopdf`

Output is written to `main/output/<doc_key>_<system_key>_<timestamp>/`.

## Supported Document Types

| doc_key              | Description              |
|----------------------|--------------------------|
| `wartungsvertrag`    | Maintenance contract     |
| `wartungsprotokoll`  | Maintenance protocol     |

## Supported System Types (`system_key`)

`KLIMAANLAGE`, `WAERMEPUMPE`, `HEIZKESSEL`, `LUEFTUNGSANLAGE`, `BRANDMELDEANLAGE`, `SPRINKLER`, `RAUCHMELDER`, `FEUERSCHUTZTUER`, `RAUCHSCHUTZ_RWA`, `SICHERHEITSBELEUCHTUNG`, `AUFZUG_PERSONEN`, `ELEKTRISCHE_ANLAGE`, `HEBEANLAGE_ABWASSER`, `NOTSTROMAGGREGAT`, `FEUERSCHUTZABSCHLUSS`, `FEUERSCHUTZEINRICHTUNG_MANUELL`, `SANITAER_ALLG`, `ELEKTRISCHE_ANLAGE_MOBIL`, `BLITZSCHUTZ`, `DRUCKBEHAELTER`, `CO_WARNANLAGE`

Each `(doc_key, system_key)` pair must have a matching requirement file at `main/document_requirements/<doc_key>/<system_key>.txt`.

## Tech Stack

- **Claude Sonnet 4.6** via AWS Bedrock (`eu.anthropic.claude-sonnet-4-6`, `eu-central-1`)
- **pdfkit / wkhtmltopdf** for HTML-to-PDF rendering
- **boto3** for AWS authentication
- **python-dotenv** for environment configuration
