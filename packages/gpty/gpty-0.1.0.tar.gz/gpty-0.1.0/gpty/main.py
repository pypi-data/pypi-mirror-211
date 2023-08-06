"""Main program entry."""
# pylint: skip-file

import sys

import click

from gpty import __version__
from gpty.gpty import Gpty
from gpty.utility import utility

MAIN_HELP_TEXT = f"""
    \t\t\t \033[93m gpty (Version: {__version__}) \033[0m

    gpty is a CLI tool that allows you to interact with the ChatGPT API
    It is designed to be easy to use on common ChatGPT developer tasks.

    QUICK START:

    \b
      1. Create a ChatGPT API key
      2. Set the OPENAI_API_KEY environment variable
      3. Run CLI tool
"""


def read_stdin():
    """Read the standard input piped into command."""
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


# -----------------------------------------------------------------------------


@click.group(help=MAIN_HELP_TEXT)
def cli():
    """Your CLI tool."""
    ...


# -----------------------------------------------------------------------------


@cli.command(short_help="\tSimple stand-alone prompt")
@click.argument("text", nargs=1, type=str, required=True, default="-")
def prompt(text):
    """Stand-alone prompt."""
    text = read_stdin() if text == "-" else text
    if not text:
        utility.fail_out("ERROR: Value PROMPT cannot be blank")
    response = Gpty().send(str(text))
    # click.secho(f"RESPONSE: {response}", fg="green")
    click.echo(response)


# -----------------------------------------------------------------------------


@cli.group(short_help="\tFile operations")
def file():
    """File operations."""
    pass


@file.command(short_help="\tChange file contents")
@click.argument("filepath", nargs=1, type=click.Path(exists=True), required=True)
@click.argument("prompt", nargs=1, type=str, required=True)
def change(filepath, prompt):
    """Prompt based on a specified file."""
    response = Gpty().file_change(filepath, prompt)
    filepath_out = utility.filename_append_text(filepath, "-gpty")
    utility.write_to_file(filepath_out, response)
    click.echo(response)


@file.command(short_help="\tExplain file contents")
@click.argument("filepath", nargs=1, type=click.Path(exists=True), required=True)
def explain(filepath):
    """Prompt based on a specified file."""
    response = Gpty().file_explain(filepath)
    # filepath_out = utility.filename_append_text(filepath, "-gpty")
    # utility.write_to_file(filepath_out, response)
    click.echo(response)


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    """Main entry point to the entire program."""
    cli()


# @cli.command(short_help="\tTESTING")
# @click.argument("filepath", nargs=1, type=click.Path(exists=True), required=True)
# @click.argument("prompt", nargs=1, type=str, required=True)
# def testing(filepath, prompt):
#     """Prompt based on a specified file."""
#     gpty = Gpty()
#     response = gpty.testing(filepath, prompt, CHANGE_FILE)
#     click.echo(response)
