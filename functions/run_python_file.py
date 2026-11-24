import os
import subprocess
from typing import Any

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
        working_dir_abs = os.path.realpath(working_directory)
        target_dir = os.path.realpath(os.path.join(working_dir_abs, file_path))

        # Ensure the target file is within the permitted working directory
        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            result = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            print(result)
            return result

        # Check that the path is a regular file
        if not os.path.isfile(target_dir):
            result = f'Error: "{file_path}" does not exist or is not a regular file'
            print(result)
            return result

        # Check that the file is a Python file
        if not file_path.endswith(".py"):
            result = f'Error: "{file_path}" is not a Python file'
            print(result)
            return result

        # Execute the Python script
        command = ["python", target_dir]
        if args:
            command.extend(args)
            
        completed_process = subprocess.run(
            command, 
            cwd=working_directory, 
            text=True, 
            timeout=30, 
            capture_output=True
        )
        
        # Handle non-zero exit codes
        if completed_process.returncode != 0:
            result = f"Process exited with code {completed_process.returncode}"
        else:
            stdout = completed_process.stdout.strip()
            stderr = completed_process.stderr.strip()
            
            if stdout or stderr:
                result = f"- STDOUT: {stdout}\n- STDERR: {stderr}"
            else:
                result = "No output produced"

        print(f"Python file executed: {file_path}")
        return result
        
    except ValueError as e:
        # Handle cases where paths are on different drives (Windows)
        result = f"Error: Invalid path operation - {e}"
        print(result)
        return result
    except Exception as e:
        # Catch any other exceptions
        result = f"Error: executing Python file: {e}"
        print(result)
        return result