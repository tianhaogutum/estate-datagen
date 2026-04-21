# Synthetic Data Generation — 1000plus

Generates synthetic German maintenance documents (Wartungsverträge, Wartungsprotokolle) using Claude AI via AWS Bedrock. The system takes seed documents as input and produces diverse, high-fidelity HTML and PDF outputs with content variation while preserving required baseline fields.

## Project Structure

```
SyntheticDataGeneration/
├── main/                              # Main pipeline
│   ├── pipeline.py                    # Entry point — orchestrates the full pipeline
│   ├── data_synthesizer.py            # LLM-based JSON data generation
│   ├── doc_generator.py               # HTML/PDF document rendering
│   ├── taxonomy.py                    # Document type definitions
│   ├── style_profiles.py              # Visual style variants (5 profiles)
│   ├── document_requirements/         # Template specifications
│   │   ├── wartungsvertrag.txt
│   │   └── wartungsprotokoll.txt
│   ├── few_shots/                     # Example PDFs for few-shot prompting
│   └── output/                        # Generated documents
├── eva/                               # Evaluation / prototyping
│   ├── main.py                        # Single document generation
│   ├── KONZEPT.md                     # Concept documentation
│   ├── utils/
│   │   └── render.py                  # HTML extraction & PDF conversion (WeasyPrint)
│   └── Daten_AI_Engineer_CaseStudy/   # Seed documents (PDF, DOCX)
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python >= 3.10
- AWS CLI installed and configured with a profile that has Bedrock access in `eu-central-1`
- WeasyPrint system dependencies ([installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html))

## Setup

### 1. Create and activate a virtual environment

**PowerShell** (run once if needed):
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

```powershell
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

Make sure you have a working AWS profile with Bedrock access:

```bash
aws configure --profile <your-profile-name>
```

Verify it works:

```bash
aws sts get-caller-identity --profile <your-profile-name>
```

## Running the Pipeline

### Full pipeline (multiple style variants)

From the repository root:

```bash
cd main
python pipeline.py                    # default: wartungsvertrag
python pipeline.py wartungsprotokoll  # maintenance protocol
```

The pipeline runs two stages:

1. **Synthesizer** — calls Claude to generate structured JSON data from document requirements
2. **Generator** — calls Claude with few-shot examples to produce HTML, then renders to PDF in 5 style variants

Output is saved to a timestamped folder in `main/output/`.

### Single document generation (eva)

```bash
cd eva
python main.py
```

## Supported Document Types

| Key                  | Description              |
|----------------------|--------------------------|
| `wartungsvertrag`    | Maintenance contract     |
| `wartungsprotokoll`  | Maintenance protocol     |

Supported equipment: heat pumps, smoke detectors, solar systems, HVAC, ventilation.

## Tech Stack

- **Claude Sonnet 4** via AWS Bedrock (`eu-central-1`)
- **WeasyPrint** for HTML-to-PDF rendering
- **boto3** for AWS authentication
- **python-dotenv** for environment configuration
