import click
import os
from openai import OpenAI
import subprocess
from click.core import Context
from bb.commands import description, branch_name
from bb.openai import OpenAIClient


def get_openai_api_key():
    try:
        return os.environ.get("OPENAI_API_KEY")
    except KeyError:
        raise ValueError("OPENAI_API_KEY environment variable is not set")


@click.group()
@click.pass_context
def cli(ctx: Context):
    client = OpenAIClient(api_key=get_openai_api_key())
    ctx.obj = dict()
    ctx.obj["client"] = client


cli.add_command(description)
cli.add_command(branch_name)
