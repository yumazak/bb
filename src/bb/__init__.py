import os
import sys
from openai import OpenAI

MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = (
    "You are an AI assistant. Generate concise Git branch names based on the user's input. "
    "Use hyphens to separate words, and include relevant context such as 'feature', 'fix', "
    "'hotfix', 'refactor', 'chore', or other common prefixes, followed by a brief description. "
    "Keep it short and readable."
)


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


def build_branch_name(client, details: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": details},
        ],
    )
    return completion.choices[0].message.content


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: bb <details>")
        return 1

    details = sys.argv[1]
    client = get_openai_client()
    branch_name = build_branch_name(client, details)
    print(branch_name)
    return 0
