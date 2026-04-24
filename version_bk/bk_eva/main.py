import base64
import subprocess
from pathlib import Path

import boto3

from version_bk.bk_eva.utils.render import extract_html_solutions_and_convert_to_pdf

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "Daten_AI_Engineer_CaseStudy"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

doc_types = ["Wartungsprotokoll", "Wartungsvertrag"]

system_types = [
    "Wärmepumpe",
    "Rauchwarnmelder",
    "Solaranlage",
    "Klimaanlage",
    "Lüftungsanlage",
]

baseline_requirements = {
    "Wartungsprotokoll": [
        "Anlagentyp",
        "Datum der Wartung",
        "Durchgeführte Arbeiten",
        "Bemerkungen",
        "Unterschriften",
    ],
    "Wartungsvertrag": [
        "Anlagentyp",
        "Auftraggeber",
        "Auftragnehmer",
        "Objekt der Wartung",
        "Vereinbarungen",
        "Laufzeit",
        "Kosten",
        "Unterschriften",
    ],
}


def load_pdf_as_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


# Convert from docx to pdf first if not already done
if not (DATA_DIR / "Wartungsvertrag-Wärmepumpe-1.pdf").exists():
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(DATA_DIR),
            str(DATA_DIR / "Wartungsvertrag-Wärmepumpe-1.docx"),
        ]
    )
if not (DATA_DIR / "Wartungsvertrag_für_Rauchwarnmelder-2.pdf").exists():
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(DATA_DIR),
            str(DATA_DIR / "Wartungsvertrag_für_Rauchwarnmelder-2.docx"),
        ]
    )

# Load the PDF files and encode them in base64
protocol_pdf_base64_1 = load_pdf_as_base64(
    DATA_DIR / "Wartungsprotokoll_Waermepumpe-1.pdf"
)
protocol_pdf_base64_2 = load_pdf_as_base64(
    DATA_DIR / "Wartungsprotokoll-Rauchwarnmelder-2.pdf"
)
contract_pdf_base64_1 = load_pdf_as_base64(
    DATA_DIR / "Wartungsvertrag-Wärmepumpe-1.pdf"
)
contract_pdf_base64_2 = load_pdf_as_base64(
    DATA_DIR / "Wartungsvertrag_für_Rauchwarnmelder-2.pdf"
)

num_solutions = 5
doc_type = "Wartungsvertrag"
system_type = "Rauchwarnmelder"

if doc_type == "Wartungsvertrag":
    seed_docs = [contract_pdf_base64_1, contract_pdf_base64_2]
    baseline_requirements = baseline_requirements["Wartungsvertrag"]
else:
    seed_docs = [protocol_pdf_base64_1, protocol_pdf_base64_2]
    baseline_requirements = baseline_requirements["Wartungsprotokoll"]

prompt = f"""
You are an AI specialized in generating multiple unique HTML documents for {doc_type} of
a {system_type} in one response.

You have been provided with seed documents in base64 format. These documents serve as
examples for the style, layout, and content of the type of document you should generate.

The generated documents should be well-formed HTML and must NOT contain duplicate
content across them.

Now, generate {num_solutions} unique HTML documents for {doc_type} of a {system_type}
that follow these rules:

1. Strictly reflect the overall style, layout, and content of the provided samples,
   but DO NOT copy any text, disclaimers, or layout verbatim.

2. Include any essential mandatory fields: {baseline_requirements}, but vary how
   they are presented (e.g., different layouts, different wording, etc.) and add
   additional elements.

3. Maintain an A4 size format for printing
   (for example using: @page {{ size: A4; }} or similar CSS).

4. Use a white background with clean and professional styling.

5. Avoid copy-pasting or reusing large chunks of HTML, CSS, or disclaimers.
   Each document must be at least 70% different in both code and text compared
   to the others.

6. Each generated document MUST be strictly wrapped in <HTML>...</HTML> tags,
   exactly like this:

   1. <HTML>...Solution #1...</HTML>
   2. <HTML>...Solution #2...</HTML>
   ...
   {num_solutions}. <HTML>...Solution #{num_solutions}...</HTML>

Additional Requirements:
- Language and content must be in GERMAN.
- Ensure each document is complete and valid.

Now generate the {num_solutions} distinct {doc_type} documents.
"""

messages = [
    {
        "role": "user",
        "content": [
            {
                "text": f"Here is the first seed document (base64 encoded PDF):\n\n{seed_docs[0]}"
            },
            {
                "text": f"Here is the second seed document (base64 encoded PDF):\n\n{seed_docs[1]}"
            },
            {"text": prompt},
        ],
    }
]

response = bedrock_client.converse(
    modelId=BEDROCK_MODEL_ID,
    messages=messages,
    inferenceConfig={"maxTokens": num_solutions * 5000, "temperature": 0.7},
)

response_text = response["output"]["message"]["content"][0]["text"]

filename = f"generated_document_00_{doc_type}_{system_type}"
filepath = str(OUTPUT_DIR / filename)

with open(filepath + ".html", "w", encoding="utf-8") as f:
    f.write(response_text)

extract_html_solutions_and_convert_to_pdf(response_text, filepath)
