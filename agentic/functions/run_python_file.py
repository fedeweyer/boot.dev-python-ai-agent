import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a python script and provides its stderr and stdout.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Python file path to execute. Path is relative to the working directory (default is the working directory itself)",
                },
                 "args": {
                    "type": "array",
                    "items": "string",
                    "description": "Optional. Script additional arguments, default = None",
                 },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            result = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            is_file = os.path.isfile(target_dir)
            if is_file is False:
                result = f'Error: "{file_path}" does not exist or is not a regular file'
            else:
                if not file_path.endswith(".py"):
                    result = f'Error: "{file_path}" is not a Python file'
                    print(result)
                    return result
                command = ["python", target_dir]
                if args:
                    command.extend(args)
                completed_process = subprocess.run(command, cwd=working_directory, text=True, timeout=30, capture_output=True)
                if completed_process.returncode != 0:
                    result = f"Process exited with code {completed_process.returncode}"
                if not completed_process.stdout and not completed_process.stderr:
                    result = "No output produced"
                result = f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        print(result)
        return result
    except KeyError:
        result = f"Error: executing Python file: {e}"
        print(result)
        return result



