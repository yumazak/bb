import click
from click.core import Context
from bb.openai import OpenAIClient
import subprocess

SYSTEM_PROMPT = (
    "You are an AI assistant. Based on the provided diff, generate a concise commit message following the GitMoji specification with a relevant prefix such as 'feat', 'fix', 'refactor', or other common prefixes. "
    "Output should be in Japanese. "
    "The format should be {prefix}:{emoji} {title}. "
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


@click.command(name="commit")
@click.pass_context
def get_commit_message(ctx: Context):
    client: OpenAIClient = ctx.obj["client"]

    diff = get_diff()
    if not diff:
        click.echo("No changes found.")
        return

    commit_message = client.chat(SYSTEM_PROMPT, diff)
    click.echo("\nSuggested Commit Message:")
    click.echo(commit_message)

    if not click.confirm("\nConfirm the result?"):
        client.clear_history()
        ctx.forward(get_commit_message)
    return
