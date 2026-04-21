import json
import boto3

BEDROCK_REGION = "eu-central-1"
BEDROCK_MODEL_ID = "eu.anthropic.claude-sonnet-4-6" #"eu.anthropic.claude-opus-4-6-v1"
PROFILE = "claude-bedrock"

_bedrock = None


def get_bedrock():
    global _bedrock
    if _bedrock is None:
        _bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
    return _bedrock


def llm_call(system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
    """Single LLM call via Bedrock."""
    client = get_bedrock()
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": 0,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    })
    resp = client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body,
    )
    result = json.loads(resp["body"].read())
    return result["content"][0]["text"]


if __name__ == "__main__":
    response = llm_call(
        system_prompt="You are a helpful assistant.",
        user_prompt="Say hello in one sentence.",
    )
    print(response)