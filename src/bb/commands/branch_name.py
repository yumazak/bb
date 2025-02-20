import click
from click.core import Context
from bb.openai import OpenAIClient
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
import pyperclip

SYSTEM_PROMPT = (
    "You are an AI assistant. Generate concise Git branch names based on the user's input, which describes the task or update. "
    "Use hyphens to separate words, and include relevant context such as 'feature', 'fix', 'docs', "
    "'hotfix', 'refactor', 'chore', or other common prefixes, followed by a brief description. "
    "Always imagine and create a suitable branch name based on the details provided. "
    "Keep it short and readable, and do not use backticks (`) in the branch name."
)


@click.command(name="bn")
@click.argument("description", nargs=1)
@click.pass_context
def get_branch_name(ctx: Context, description: str):
    """Generate a branch name based on the input."""

    client: OpenAIClient = ctx.obj["client"]
    console: Console = ctx.obj["console"]

    branch_name = client.chat(SYSTEM_PROMPT, description)
    console.print(Panel(Text("Suggested Branch Name", style="green"), expand=False))
    console.print(branch_name)

    if click.confirm("\nConfirm the result?", default=True):
        pyperclip.copy(branch_name)
        console.print(Text("Branch name copied to clipboard!", style="green"))

    else:
        client.clear_history()
        ctx.forward(get_branch_name)
