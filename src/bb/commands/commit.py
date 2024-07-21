import click
from click.core import Context
from bb.openai import OpenAIClient
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import subprocess
import pyperclip

SYSTEM_PROMPT = (
    "You are an AI assistant. Based on the provided diff, generate a concise commit message. "
    "Output should be in Japanese. "
    "Only output the commit message and nothing else. "
    "Exclude any explanations, justifications, or conclusions."
)


def get_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "-w", "--ignore-blank-lines", "-U0", "HEAD"],
        capture_output=True,
        text=True,
    )
    return result.stdout


@click.command(name="co")
@click.pass_context
def get_commit_message(ctx: Context):
    """Generate a commit message based on the diff."""

    client: OpenAIClient = ctx.obj["client"]
    console: Console = ctx.obj["console"]

    diff = get_diff()
    if not diff:
        click.echo("No changes found.")
        return

    commit_message = client.chat(SYSTEM_PROMPT, diff)
    console.print(Panel(Text("Suggested Commit Message", style="green"), expand=False))
    console.print(commit_message)

    if click.confirm("\nConfirm the result?", default=True):
        pyperclip.copy(commit_message)
        console.print(Text("Commit message copied to clipboard!", style="green"))
    else:
        client.clear_history()
        ctx.forward(get_commit_message)
    return
