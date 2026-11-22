import os
import shutil

schema_delete_directory = {
    "type": "function",
    "function": {
        "name": "delete_directory",
        "description": "Deletes a directory and all its contents in the working directory with validation checks.",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Directory path to work in. Defaults to the current working directory.",
                },
                "directory_path": {
                    "type": "string",
                    "description": "Directory path to delete. Path is relative to the working directory.",
                },
            },
        },
    },
}


def delete_directory(working_directory: str, directory_path: str) -> str:
    try:
        working_dir_abs = os.path.realpath(working_directory)
        target_path = os.path.realpath(os.path.join(working_dir_abs, directory_path))

        # Ensure the target path is within the permitted working directory
        try:
            is_within_working_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        except ValueError:
            result = f'Error: Cannot delete "{directory_path}" as it is outside the permitted working directory'
            print(result)
            return result

        if not is_within_working_dir:
            result = f'Error: Cannot delete "{directory_path}" as it is outside the permitted working directory'
            print(result)
            return result

        # Check if target exists
        if not os.path.exists(target_path):
            result = f'Error: Directory "{directory_path}" does not exist'
            print(result)
            return result

        # Check if target is a directory
        if not os.path.isdir(target_path):
            result = f'Error: "{directory_path}" is not a directory'
            print(result)
            return result

        # Delete the directory and all its contents
        shutil.rmtree(target_path)
        result = f'Successfully deleted directory "{directory_path}"'
        print(f'Directory deleted: {directory_path}')
        return result

    except OSError as e:
        result = f"Error: failed to delete directory - {e}"
        print(result)
        return result
    except Exception as e:
        result = f"Error: unexpected error deleting directory - {e}"
        print(result)
        return result
