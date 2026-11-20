import os
from pathlib import Path
MAX_CHARS = 10_000

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the content of a file, limited to 10k characters, if that happens, the file is truncated and a legend indicating that is added at the end",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get content. Path is relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            result = f'Error: Cannot read "{target_dir}" as it is outside the permitted working directory'
        else:
            if not os.path.isfile(target_dir):
                result = f'Error: File not found or is not a regular file: "{target_dir}"'
            else:
                with open(target_dir, "r") as f:
                    result = f.read(MAX_CHARS)
                    # After reading the first MAX_CHARS...
                    if f.read(1):
                        result += f'[...File "{target_dir}" truncated at {MAX_CHARS} characters]'
        print(result)
        return result
    except KeyError:
        result = ("Error: failed to get_file_content")
        print(result)
        return result




