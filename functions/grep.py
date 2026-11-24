import os

schema_grep = {
    "type": "function",
    "function": {
        "name": "grep",
        "description": "Searches for files containing a text pattern in a directory, similar to grep command.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to search in, relative to the working directory (default is the working directory itself)",
                },
                "pattern": {
                    "type": "string",
                    "description": "Text pattern to search for",
                },
                "file_extension": {
                    "type": "string",
                    "description": "Optional. Only search files with this extension (e.g., .py, .txt)",
                },
            },
            "required": ["pattern"],
        },
    },
}


def grep(working_directory: str, pattern: str, directory: str = ".", file_extension: str | None = None) -> str:
    try:
        working_dir_abs = os.path.realpath(working_directory)
        target_dir = os.path.realpath(os.path.join(working_dir_abs, directory))

        # Ensure the target directory is within the allowed working directory
        try:
            is_within_working_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        except ValueError:
            result = f'Error: Cannot search in "{directory}" as it is outside the permitted working directory'
            print(result)
            return result

        if not is_within_working_dir:
            result = f'Error: Cannot search in "{directory}" as it is outside the permitted working directory'
            print(result)
            return result

        if not os.path.isdir(target_dir):
            result = f'Error: "{directory}" is not a directory'
            print(result)
            return result

        if not pattern:
            result = "Error: No search pattern provided"
            print(result)
            return result

        matches = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file_extension and not file.endswith(file_extension):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if pattern in line:
                                rel_path = os.path.relpath(file_path, working_dir_abs)
                                matches.append(f"{rel_path}:{line_num}: {line.rstrip()}")
                except (UnicodeDecodeError, PermissionError, OSError):
                    # Skip binary files or files with permission issues
                    continue

        if not matches:
            result = "No matches found"
        else:
            result = "\n".join(matches)

        print(f"Grep search completed in: {directory}")
        return result

    except Exception as exc:  # noqa: BLE001 – unexpected errors
        error_msg = f"Error: failed to perform grep search – {exc}"
        print(error_msg)
        return error_msg