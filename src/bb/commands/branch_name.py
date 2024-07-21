import click
from click.core import Context
from bb.openai import OpenAIClient
import subprocess

SYSTEM_PROMPT = (
    "You are an AI assistant. Generate concise Git branch names based on the user's input. "
    "Use hyphens to separate words, and include relevant context such as 'feature', 'fix', 'docs', "
    "'hotfix', 'refactor', 'chore', or other common prefixes, followed by a brief description. "
    "Keep it short and readable."
)

SYSTEM_PROMPT_WITH_DIFF = (
    "You are an AI assistant. Based on the provided git diff, generate a concise and appropriate Git branch name. "
    "Use hyphens to separate words, and include relevant context such as 'feature', 'fix', 'docs', "
    "'hotfix', 'refactor', 'chore', or other common prefixes, followed by a brief description. "
    "Keep it short and readable. Ensure the branch name reflects the main changes or purpose indicated by the diff."
)


def get_diff(branch_name: str) -> str:
    result = subprocess.run(
        ["git", "diff", branch_name],
        capture_output=True,
        text=True,
    )
    return result.stdout


@click.command(name="name")
@click.argument("description", nargs=1)
@click.option(
    "-b",
    "--branch",
    default="develop",
    show_default=True,
    help="Diff with this branch.",
)
@click.option("-d", "--diff", is_flag=True, help="Use diff from the current branch.")
@click.pass_context
def branch_name(ctx: Context, description: str, branch: str, diff: bool):
    client: OpenAIClient = ctx.obj["client"]

    branch_name = client.chat(SYSTEM_PROMPT, description)
    click.echo(branch_name)
