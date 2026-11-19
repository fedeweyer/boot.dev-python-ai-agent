import os
from pathlib import Path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:

        working_dir_abs =  os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.isdir(target_dir):
            result = f'Error: "{directory}" is not a directory'
            print(result)
            return result

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            result = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            result = f'Success: "{directory}" is within the working directory'
        print(result)
        return result
    except KeyError:
        result = ("Error: failed to get_files_info")
        print(result)
        return result
