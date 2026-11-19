import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            result = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'


        else:
            is_dir = os.path.isdir(target_dir)
            if is_dir is True:
                result = f'Error: Cannot write to "{file_path}" as it is a directory'
            else:
                os.makedirs(os.path.dirname(target_dir), exist_ok=True)
                with open(target_dir, "w") as f:
                    f.write(content)
                result = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        print(result)
        return result
    except KeyError:
        result = ("Error: failed to get_file_content")
        print(result)
        return result


