import os
import sys
from bb.openai import OpenAIClient
from bb.cli import cli

MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = (
    "You are an AI assistant. Generate concise Git branch names based on the user's input. "
    "Use hyphens to separate words, and include relevant context such as 'feature', 'fix', 'docs', "
    "'hotfix', 'refactor', 'chore', or other common prefixes, followed by a brief description. "
    "Keep it short and readable."
)


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
    cli()

    return 0
