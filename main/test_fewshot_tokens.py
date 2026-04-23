"""
Check approximate token count for few-shot PDF files via Bedrock.
Sends each PDF as a document block and reads back the token usage.
"""

import platform
from pathlib import Path

import boto3

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6"

if platform.system() == "Windows":
    _session = boto3.Session(profile_name="claude-bedrock", region_name=BEDROCK_REGION)
    client = _session.client("bedrock-runtime")
else:
    client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

FEW_SHOTS = [
    "few_shots/Wartungsprotokoll_Waermepumpe-1.pdf",
    "few_shots/Wartungsprotokoll-Rauchwarnmelder-2.pdf",
    "few_shots/Wartungsvertrag-Wärmepumpe-1.pdf",
    "few_shots/Wartungsvertrag_für_Rauchwarnmelder-2.pdf",
]

base = Path(__file__).parent


def count_tokens(pdf_path: Path) -> dict:
    block = {
        "document": {
            "format": "pdf",
            "name": pdf_path.stem[:50],
            "source": {"bytes": pdf_path.read_bytes()},
        }
    }
    response = client.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[
            {"role": "user", "content": [block, {"text": "Summarize in one word."}]}
        ],
        inferenceConfig={"maxTokens": 5},
    )
    usage = response["usage"]
    return {
        "input_tokens": usage["inputTokens"],
        "output_tokens": usage["outputTokens"],
    }


if __name__ == "__main__":
    total_input = 0
    for rel in FEW_SHOTS:
        p = (base / rel).resolve()
        if not p.exists():
            print(f"MISSING: {rel}")
            continue
        result = count_tokens(p)
        input_tok = result["input_tokens"]
        total_input += input_tok
        print(f"{p.name}: {input_tok:,} input tokens")

    print(f"\nTotal input tokens (all 4 PDFs + prompt): {total_input:,}")
