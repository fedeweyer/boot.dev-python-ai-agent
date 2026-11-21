"""Function calling module for handling tool calls from the LLM."""

import json
import logging
from collections.abc import Callable
from typing import Any

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

# Configure logger
logger = logging.getLogger(__name__)

# Function schemas for LLM function calling
AVAILABLE_FUNCTIONS = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

# Map of function names to their implementations
FUNCTION_MAP: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(tool_call: Any, verbose: bool = False) -> dict:
    """
    Execute a function call from the LLM.

    Args:
        tool_call: The tool call object from the LLM containing function name and arguments.
        verbose: If True, log detailed function call information.

    Returns:
        A dictionary containing the function result formatted for the LLM.
    """
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    function_args["working_directory"] = "./calculator"
    if verbose is True:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        logger.info("Calling function: %s", function_name)

    func = FUNCTION_MAP.get(function_name)
    if func is None:
        error_msg = f"Error: Unknown function: {function_name}"
        logger.error(error_msg)
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": error_msg,
        }

    try:
        result = func(**function_args)
    except Exception as e:
        error_msg = f"Error executing {function_name}: {e}"
        logger.exception(error_msg)
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": error_msg,
        }

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
