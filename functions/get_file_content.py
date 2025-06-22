import os
from config import MAX_CHAR


def get_file_content(working_directory, file_path):
    
    wd_abs = os.path.abspath(working_directory)
    dir_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not (dir_abs == wd_abs or dir_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(dir_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(dir_abs, "r") as f:
            file_content_string = f.read(MAX_CHAR)
            islonger = f.read(1)
    
    except Exception as e:
        return f"Error: {e}"
    
    if len(islonger) > 0:
        file_content_string += f'''\n[...File "{file_path}" truncated at 10000 characters]'''
    
    return file_content_string