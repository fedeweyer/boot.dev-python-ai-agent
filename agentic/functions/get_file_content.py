import os

MAX_FILE_CONTENT_CHARS = 10_000


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the content of a file, limited to 10k characters. Truncation is indicated with a marker if the file exceeds the limit.",
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
    """Read and return the content of a file, truncated at MAX_FILE_CONTENT_CHARS if needed.

    Args:
        working_directory: The base directory for resolving relative paths.
        file_path: Path to the file to read, relative to working_directory.

    Returns:
        File content as a string, or an error message starting with "Error:".
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Ensure the target file is within the permitted working directory
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            result = f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
            print(result)
            return result

        # Check that the path is a regular file within the working directory
        if not os.path.isfile(target_file):
            result = f'Error: File not found or is not a regular file: "{target_file}"'
            print(result)
            return result

        with open(target_file, "r") as f:
            result = f.read(MAX_FILE_CONTENT_CHARS)
            # If there's more content beyond the limit, append a truncation marker
            if f.read(1):
                result += f'[...File "{target_file}" truncated at {MAX_FILE_CONTENT_CHARS} characters]'

        print(result)
        return result

    except Exception as e:
        result = f"Error: failed to get_file_content - {e}"
        print(result)
        return result