import boto3
import base64
import subprocess
import os

from dotenv import load_dotenv

from utils.render import extract_html_solutions_and_convert_to_pdf

# Load environment variables and initialize the AWS Bedrock client
load_dotenv()

# AWS Bedrock configuration
AWS_REGION = os.getenv('AWS_REGION', 'eu-central-1')
bedrock_client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=AWS_REGION
)

# Bedrock model ID for Claude (using inference profile)
BEDROCK_MODEL_ID = 'eu.anthropic.claude-sonnet-4-6'

# Define document types, system types, and baseline requirements for the generated documents.
# These will be used in the prompt to guide the generation of the HTML documents.
# Could be done in a more automated way by extractig and anlyzing the text and structure of the sample documents.
# For the prototype, I have manually analyzed the documents and enlarged the list of system types. 

doc_types = ["Wartungsprotokoll", "Wartungsvertrag"]

system_types = ["Wärmepumpe", "Rauchwarnmelder", "Solaranlage", "Klimaanlage", "Lüftungsanlage"]

baseline_requirements = {
    "Wartungsprotokoll": [
        "Anlagentyp",
        "Datum der Wartung",
        "Durchgeführte Arbeiten",
        "Bemerkungen",
        "Unterschriften"
    ],
    "Wartungsvertrag": [
        "Anlagentyp",
        "Auftraggeber",
        "Auftragnehmer",
        "Objekt der Wartung",
        "Vereinbarungen",
        "Laufzeit",
        "Kosten",
        "Unterschriften"
    ]
}

# Function to load a PDF file and encode it in base64 to include in the prompt as a seed document
def load_pdf_as_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

# Convert from docx to pdf first if not already done 
if not os.path.exists("Daten_AI_Engineer_CaseStudy/Wartungsvertrag-Wärmepumpe-1.pdf"):
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", "Daten_AI_Engineer_CaseStudy", "Daten_AI_Engineer_CaseStudy/Wartungsvertrag-Wärmepumpe-1.docx"])
if not os.path.exists("Daten_AI_Engineer_CaseStudy/Wartungsvertrag_für_Rauchwarnmelder-2.pdf"):
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", "Daten_AI_Engineer_CaseStudy", "Daten_AI_Engineer_CaseStudy/Wartungsvertrag_für_Rauchwarnmelder-2.docx"])

# Load the PDF files and encode them in base64
protocol_pdf_base64_1 = load_pdf_as_base64("Daten_AI_Engineer_CaseStudy/Wartungsprotokoll_Waermepumpe-1.pdf")
protocol_pdf_base64_2 = load_pdf_as_base64("Daten_AI_Engineer_CaseStudy/Wartungsprotokoll-Rauchwarnmelder-2.pdf")
contract_pdf_base64_1 = load_pdf_as_base64("Daten_AI_Engineer_CaseStudy/Wartungsvertrag-Wärmepumpe-1.pdf")
contract_pdf_base64_2 = load_pdf_as_base64("Daten_AI_Engineer_CaseStudy/Wartungsvertrag_für_Rauchwarnmelder-2.pdf")

# Define the prompt for generating multiple unique HTML documents
num_solutions = 5
doc_type = "Wartungsvertrag" # Set or select from doc_types
system_type = "Rauchwarnmelder" # Set or select from system_types

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

# Generate the HTML documents using AWS Bedrock Claude model
# Build messages for Bedrock (convert base64 PDFs to text content)
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
            {
                "text": prompt
            }
        ]
    }
]

# Call Bedrock API
response = bedrock_client.converse(
    modelId=BEDROCK_MODEL_ID,
    messages=messages,
    inferenceConfig={
        'maxTokens': num_solutions * 5000,
        'temperature': 0.7
    }
)

# Extract the response text
response_text = response['output']['message']['content'][0]['text']

# Define the filename and filepath for saving the generated HTML content and PDF
filename = f"generated_document_00_{doc_type}_{system_type}"
filepath = "output/" + filename

# Save the generated HTML content to a file
with open(filepath + ".html", "w") as f:
    f.write(response_text)

# Render the generated HTML documents to PDF
extract_html_solutions_and_convert_to_pdf(response_text, filepath)
