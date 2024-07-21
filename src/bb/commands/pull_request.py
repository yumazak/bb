import click
from click.core import Context
from bb.openai import OpenAIClient
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

SYSTEM_PROMPT_DESCRIPTION = (
    "You are an AI assistant. Based on the provided diff, generate a concise list of changes for a pull request comment. "
    "Summarize and briefly describe the main improvements or fixes. "
    "Output should be in Japanese, formatted in a simple and readable list without numbering. "
    "Exclude any additional explanations, justifications, or conclusions. "
    "Only list the changes, keeping package management changes simple."
)


SYSTEM_PROMPT_BRANCH_NAME = (
    "You are an AI assistant. Based on the provided git diff, generate a concise and appropriate Git branch name. "
    "Use hyphens to separate words, and include relevant context such as 'feature', 'fix', 'docs', "
    "'hotfix', 'refactor', 'chore', or other common prefixes, followed by a brief description. "
    "Keep it short and readable. Ensure the branch name reflects the main changes or purpose indicated by the diff."
)


SYSTEM_PROMPT_PR_NAME = (
    "You are an AI assistant. Based on the provided diff, generate a concise pull request name following the GitMoji specification with a relevant prefix such as 'feat', 'fix', 'refactor', or other common prefixes. "
    "Output should be in Japanese. "
    "The format should be {prefix}:{emoji} {title}. "
    "Only output the pull request title and nothing else. "
    "Exclude any explanations, justifications, or conclusions."
)


def get_diff(branch_name: str) -> str:
    result = subprocess.run(
        ["git", "diff", "-w", "--ignore-blank-lines", "-U0", branch_name],
        capture_output=True,
        text=True,
    )
    return result.stdout


@click.command(name="pr")
@click.option(
    "-b",
    "--branch",
    default="develop",
    show_default=True,
    help="Diff with this branch.",
)
@click.option(
    "-t",
    "--title",
    is_flag=True,
    default=False,
    help="Generate a pull request title based on the diff.",
)
@click.option(
    "-n",
    "--name",
    is_flag=True,
    default=False,
    help="Generate a branch name based on the diff.",
)
@click.pass_context
def pull_request(ctx: Context, branch: str, title: bool, name: bool):
    """Generate a pull request description, title, and branch name based on the diff."""

    client: OpenAIClient = ctx.obj["client"]
    console: Console = ctx.obj["console"]

    diff = get_diff(branch)
    if not diff:
        console.print("[bold red]No changes found.[/bold red]")
        return

    diff_description = client.chat(SYSTEM_PROMPT_DESCRIPTION, diff)
    console.print(Panel(Text("Pull Request Description", style="green"), expand=False))
    console.print(diff_description)

    if title:
        pr_title = client.chat(SYSTEM_PROMPT_PR_NAME, diff)
        console.print(Panel(Text("Pull Request Title", style="blue"), expand=False))
        console.print(pr_title)

    if name:
        branch_name = client.chat(SYSTEM_PROMPT_BRANCH_NAME, diff)
        console.print(Panel(Text("Branch Name", style="cyan"), expand=False))
        console.print(branch_name)

    if not click.confirm("\nConfirm the result?", default=True):
        client.clear_history()
        ctx.forward(pull_request)
    return
