"""General utility and tools."""

import json
import logging
import os
import sys
from functools import wraps
from pathlib import Path
from string import Template
from typing import Any, Dict, Union

import requests
import toml
import yaml
from click import echo, style
from yaspin import yaspin
from yaspin.spinners import Spinners

logger = logging.getLogger()


def print2(message: Any, bold: bool = False, color: str = "reset") -> None:
    """Print a message to the console using click.

    Details:
        - Colors: `black` (might be a gray), `red`, `green`, `yellow` (might be an orange), `blue`,
          `magenta`, `cyan`, `white` (might be light gray), `reset` (reset the color code only)

    Example Usage:
        - `print2("Hey there!", bold=True, color="green")`

    Args:
        message: Message to print to console
        bold   : Whether to bold the message
        color  : Color to use for the message ()
    """
    echo(style(message, fg=color, bold=bold))


def warn_out(message: str) -> None:
    """Output one warning message to the console.

    Example Usage:
        - `warn_out("Something went wrong!")`

    Args:
        message: Message to output to console
    """
    echo(style(message, fg="bright_yellow", bold=True))


def fail_out(message: str) -> None:
    """Output one failure message to the console, then exit.

    Example Usage:
        - `fail_out("Something went wrong!")`

    Args:
        message: Message to output to console
    """
    echo(style(message, fg="bright_red", bold=True))
    sys.exit(1)


def failures_out(messages: list) -> None:
    """Output multiple failure messages to the console, then exit.

    Example Usage:
        - `failures_out(["Oh no!", "This is not good!"])`

    Args:
        message: Multiple messages to output to console
    """
    for message in messages:
        echo(style(message, fg="bright_red", bold=True))
    sys.exit(1)


def load_contents_from_local_file(local_file_path: str, file_type: str = "txt") -> Dict:
    """Load a local file contents.

    Parameters:
        local_file_path (str) : Path to a local TOML file to be loaded
        file_type (str)       : Type of file to be loaded ie. 'yaml', 'toml', 'json'
    Returns:
        file_contents (dict) : The contents of file
    """
    file_type = file_type.lower()

    # Check if file exists
    if not os.path.isfile(local_file_path):
        fail_out(f"Failed to find file: {local_file_path}")

    # Check if file is completely empty
    if os.stat(local_file_path).st_size == 0:
        return {}

    logger.debug(f"Loading specified local .{file_type} file: '{local_file_path}' ...")
    try:
        with open(local_file_path, "r", encoding="utf-8") as open_file:
            if file_type == "yaml":
                file_contents = yaml.safe_load(open_file)
            elif file_type == "toml":
                file_contents = toml.load(open_file)
            elif file_type == "json":
                file_contents = json.loads(open_file.read())
            else:
                # Plain text file
                file_contents = open_file.read()
        logger.debug(f"Successfully loaded local .{file_type} file")
    except Exception as error:
        fail_out(
            f"Failed to load specified local .{file_type} "
            f"file: '{local_file_path}'. Exception: {error}"
        )

    return file_contents


def load_contents_from_string(file_type: str, text: str) -> Dict:
    """Loading a local file contents

    Parameters:
        file_type (str) : Type of file to be loaded ie. 'yaml', 'toml', 'json'
        text (str)      : Text string to be loaded as specified filetype
    Returns:
        contents (dict) : The contents of file
    """
    file_type = file_type.lower()
    logger.debug(f"Loading specified text string as filetype '{file_type}' ...")
    if file_type == "yaml":
        contents = yaml.safe_load(text)
    elif file_type == "toml":
        contents = toml.loads(text)
    elif file_type == "json":
        contents = json.loads(text)
    else:
        raise ValueError(f'Unknown file type passed: "{file_type}"')
    logger.debug(f'Successfully loaded specified "{file_type}" contents from text string')
    return contents


def load_contents_from_remote_file_url(
    file_type: str, remote_file_url: str, allow_redirects: bool = True
) -> Dict:
    """Loading a remote yaml file contents over HTTP.

    ### FIXME: Make it able to load toml, json, and yaml file types

    Args:
        file_type (str)       : Type of file to be loaded ie. 'yaml', 'toml', 'json'
        remote_file_url (url)  : Remote URL location of file to be loaded
        allow_redirects (bool) : If True allow redirects to another URL (default True)
    Returns:
        file_contents (Dict) : The contents of the file
    """
    file_type = file_type.lower()

    # Getting name of file from URL
    remote_filename = Path(remote_file_url).name
    logger.debug(f"Requested remote filename parsed: {remote_filename}")

    # Check requested file extension
    remote_file_ext = Path(remote_file_url).suffix
    file_ext_accepted = [".yml", ".yaml", ".conf"]
    if not remote_file_ext in file_ext_accepted:
        logger.debug(
            f'Remote file requested "{remote_filename}"" is not one '
            f"of the accepted file types: {file_ext_accepted}"
        )
        return {}

    # Get request headers
    logger.debug(f'Getting remote file HTTP request headers for "{remote_file_url}" ...')
    try:
        return_content = requests.head(remote_file_url)
    except Exception as error:
        logger.debug(f"Failed to request headers. Exception: {error}")
        return {}
    header = return_content.headers

    # Check if file is below size limit
    content_length = int(header["Content-length"]) / 1000000
    logger.debug(f"Requested file content length: {content_length:.5f} MB)")
    if content_length > 1.0:
        logger.debug(
            f'The requested remote file "{remote_filename}" is {content_length:.2f} MB and larger than 1.0 MB limit, will not download'
        )
        return {}

    # Check if content is text or yaml based
    content_types_accepted = [
        "text/plain",
        "text/x-yaml",
        "application/x-yaml",
        "text/yaml",
        "text/vnd.yaml",
    ]
    content_type = header.get("content-type")
    logger.debug(f"Request content type: {content_type}")
    if not content_type:
        return {}
    elif not any(ext in content_type for ext in content_types_accepted):
        logger.debug(
            f'The content type "{content_type}" of the requested file "{remote_filename}" is not one of the following: {content_types_accepted}'
        )
        return {}

    # Downloading the file content
    logger.debug(f"Requesting remote file: '{remote_file_url}' ...")
    remote_request = requests.get(remote_file_url, allow_redirects=allow_redirects)

    # Check if no error from downloading
    if remote_request.status_code == requests.codes.ok:
        # Loading the yaml file content
        logger.debug("Loading contents of remote file ...")
        try:
            file_contents = yaml.safe_load(remote_request.content)
        except Exception as error:
            logger.debug(f"Failed loading requested file. Exception: {error}")
            return {}
    else:
        logger.debug(
            f"Failed to get remote file '{remote_file_url}'. HTTP request "
            f"error code {remote_request.status_code}"
        )
        return {}

    return file_contents


def template_apply(string_template: str, **kwargs: dict) -> str:
    """Apply/Fill variables into a string template.
    Placeholder variables must be in the `${variable_name}` format.

    Details:
        - Example of a string template:
            `'{
                "credentials": {
                    "scope": "${domain}",
                    "username": "${username}"
                }'`

    Args:
        string_template: A string template with placeholders (ie. `${variable}`)
        kwargs: dictionary of variables to be applied

    Returns:
        String template with variables applied
    """
    logger.debug("Applying variables to string template ...")
    logger.debug(f'Applied variables: {", ".join(list(kwargs.keys()))}')
    # Replace None with empty string
    for key, value in kwargs.items():
        if value is None:
            kwargs[key] = ""

    template = Template(string_template)
    try:
        template_filled = template.safe_substitute(**kwargs)
    except Exception as error:
        logger.debug(f"Failed to apply variables to string template. Exception: {error}")
        return ""

    logger.debug("Successfully applied variables to string template")
    return template_filled


def write_to_file(file_path: str, file_contents: str) -> bool:
    """Write file contents to a file.

    Args:
        file_path     : Path to file to be written
        file_contents : Contents to be written to file
    Returns:
        success (bool)      : True if file was successfully written
    """
    logger.debug(f"Writing contents to file '{file_path}' ...")
    try:
        with open(file_path, "w", encoding="utf-8") as open_file:
            open_file.write(file_contents)
    except (IOError, PermissionError) as error:
        logger.debug(f"Failed to write contents to file. Exception: {error}")
        return False
    logger.debug("Successfully wrote contents to file")
    return True


def filename_append_text(filepath: str, text: str) -> str:
    """Append text to a filename only.

    Args:
        filepath : Path to file to be appended
        text     : Text to be appended to filename
    Returns:
        new_file_path (str) : New file path with text appended to filename
    """
    logger.debug(f"Appending text to filename '{filepath}' ...")
    filepath = Path(filepath)
    new_file_path = filepath.parent / f"{filepath.stem}{text}{filepath.suffix}"
    logger.debug(f"New file path: '{new_file_path}'")
    return str(new_file_path)


def with_spinner(message):
    """Decorator to add a spinner to a function.

    Args:
        message: Message to be displayed with spinner
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            spinner = yaspin(spinner=getattr(Spinners, "bouncingBar"), attrs=["bold"], text=message)
            spinner.start()
            try:
                result = function(*args, **kwargs)
                return result
            finally:
                spinner.stop()

        return wrapper

    return decorator
