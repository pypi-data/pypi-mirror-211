"""Gpty class definition."""

import logging
import os
import sys

import click
import openai
from openai.error import OpenAIError

from gpty.gpty import prompt_templates
from gpty.utility import utility

logger = logging.getLogger()


class Gpty:
    """Gpty class definition."""

    def __init__(self) -> None:
        """Gpty object."""
        self._load_api_key()

    def _load_api_key(self) -> None:
        """Load API key from environment variable."""
        if "OPENAI_API_KEY" not in os.environ:
            click.secho('ERROR: Environmental variable "OPENAI_API_KEY" is not set', fg="red")
            click.secho(
                '       If you do not have a OpenAI API key, you can get one in your '
                'OpenAI account under "View API keys". Note that charges may apply.',
                fg="red"
            )
            sys.exit(1)
        openai.api_key = os.environ["OPENAI_API_KEY"]

    # def _file_compile_prompt(self, filepath: str, prompt: str, prompt_template: str) -> str:
    def _file_compile_prompt(self, filepath: str, prompt_template: str, **kwargs) -> str:
        """Prompt based on a specified file.

        Args:
            filepath: Path to local file
            prompt_template: Template to apply to prompt text
            kwargs: Any additional keyword arguments to pass to template
        """
        file_contents = utility.load_contents_from_local_file(filepath)
        prompt_out = utility.template_apply(
            string_template=prompt_template,
            file_contents=file_contents,
            **kwargs,
        )
        return prompt_out

    def file_change(self, filepath, prompt):
        """Prompt based on a specified file."""
        prompt = self._file_compile_prompt(filepath, prompt_templates.CHANGE_FILE, prompt=prompt)
        return self.send(prompt)

    def file_explain(self, filepath):
        """Prompt based on a specified file."""
        prompt = self._file_compile_prompt(filepath, prompt_templates.EXPLAIN_FILE)
        return self.send(prompt)

    @utility.with_spinner("Waiting on ChatGPT API completion ...")
    def send(self, prompt: str, engine: str = "text-davinci-003", choice: int = 0) -> str:
        """Send completion prompt to ChatGPT API.

        Args:
            prompt: Prompt text
            engine: ChatGPT engine
            choice: Choice of response from API

        Returns:
            Response from API
        """
        # engine      - OpenAI engine to use
        # prompt      - Text to generate completions for (required)
        # max_tokens  - Maximum number of tokens to generate
        # n           - Number of completions to generate
        # stop        - Sequence of tokens where the API will stop generating further tokens
        # temperature - Controls randomness: Lowering results in less random completions.
        #               As the temperature approaches zero, the model will become
        #               deterministic and repetitive. Higher temperature results in more
        #               random completions.
        # top_p       - Controls diversity via nucleus sampling: 0.5 means half of all
        #                1.0 effectively disables this sampling
        # frequency_penalty - Float that penalizes new tokens based on their existing frequency
        # presence_penalty  - Float that penalizes new tokens based on whether they appear in the
        #                    text so far. Decreases the model's likelihood to repeat the same line
        #                    verbatim.
        try:
            response = (
                openai.Completion.create(
                    engine=engine,
                    prompt=prompt,
                    max_tokens=1000,
                    n=1,
                    stop=None,
                    temperature=0.4,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                .choices[choice]
                .text.strip()
            )
        except OpenAIError as error:
            # yaspin.stop_all()
            utility.fail_out(f"SERVER ERROR: {error}")

        return response
