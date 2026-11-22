import os
from pathlib import Path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.realpath(working_directory)
        target_dir = os.path.realpath(os.path.join(working_dir_abs, directory))

        # Ensure the target directory is within the allowed working directory
        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            error_msg = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            print(error_msg)
            return error_msg

        if not os.path.isdir(target_dir):
            error_msg = f'Error: "{directory}" is not a directory'
            print(error_msg)
            return error_msg

        entries: list[str] = []
        for entry in Path(target_dir).iterdir():
            file_size = entry.stat().st_size
            is_dir = entry.is_dir()
            entries.append(f"- {entry.name}: file_size= {file_size} bytes, is_dir={is_dir}")

        result = "\n".join(entries)
        print(f"Listed files in: {directory}")
        return result

    except Exception as exc:  # noqa: BLE001 – unexpected errors
        error_msg = f"Error: failed to get_files_info – {exc}"
        print(error_msg)
        return error_msg
