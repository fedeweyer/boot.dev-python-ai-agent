import os

schema_delete_file = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "description": "Deletes a file in the working directory with validation checks.",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Directory path to work in. Defaults to the current working directory.",
                },
                "file_path": {
                    "type": "string",
                    "description": "File path to delete. Path is relative to the working directory.",
                },
            },
        },
    },
}


def delete_file(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.realpath(working_directory)
        target_path = os.path.realpath(os.path.join(working_dir_abs, file_path))

        # Ensure the target path is within the permitted working directory
        try:
            is_within_working_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        except ValueError:
            result = f'Error: Cannot delete "{file_path}" as it is outside the permitted working directory'
            print(result)
            return result

        if not is_within_working_dir:
            result = f'Error: Cannot delete "{file_path}" as it is outside the permitted working directory'
            print(result)
            return result

        # Check if target is a directory
        if os.path.isdir(target_path):
            result = f'Error: Cannot delete "{file_path}" as it is a directory'
            print(result)
            return result

        # Check if file exists
        if not os.path.exists(target_path):
            result = f'Error: File "{file_path}" does not exist'
            print(result)
            return result

        # Check if file is a regular file
        if not os.path.isfile(target_path):
            result = f'Error: "{file_path}" is not a regular file'
            print(result)
            return result

        # Delete the file
        os.remove(target_path)
        result = f'Successfully deleted "{file_path}"'
        return result

    except OSError as e:
        result = f"Error: failed to delete file - {e}"
        print(result)
        return result
    except Exception as e:
        result = f"Error: unexpected error deleting file - {e}"
        print(result)
        return result
