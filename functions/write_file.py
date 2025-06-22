import os

def write_file(working_directory, file_path, content):

    wd_abs = os.path.abspath(working_directory)
    dir_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not (dir_abs == wd_abs or dir_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        d_name = os.path.dirname(dir_abs)
        os.makedirs(d_name, exist_ok=True)
        
        with open(dir_abs, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'