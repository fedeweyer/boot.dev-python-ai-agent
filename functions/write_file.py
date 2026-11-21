import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes a new file or overrides an existing one.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute. Path is relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "file content to write",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Ensure the target path is within the permitted working directory
        # os.path.commonpath raises ValueError on Windows if paths are on different drives
        try:
            is_within_working_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        except ValueError:
            result = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            print(result)
            return result

        if not is_within_working_dir:
            result = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            print(result)
            return result

        # Check if target is a directory
        if os.path.isdir(target_path):
            result = f'Error: Cannot write to "{file_path}" as it is a directory'
            print(result)
            return result

        # Create parent directories if they don't exist
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # Write the file
        with open(target_path, "w") as f:
            f.write(content)

        result = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        print(result)
        return result

    except OSError as e:
        result = f"Error: failed to write file - {e}"
        print(result)
        return result
    except Exception as e:
        result = f"Error: unexpected error writing file - {e}"
        print(result)
        return result
