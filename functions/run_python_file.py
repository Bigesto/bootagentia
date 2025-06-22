import os
import string
import subprocess

def run_python_file(working_directory, file_path):
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    wd_abs = os.path.abspath(working_directory)
    dir_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not (dir_abs == wd_abs or dir_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(dir_abs):
        return f'Error: File "{file_path}" not found.'
    
    try:
        results = subprocess.run(["python3", file_path], timeout=30, capture_output=True, text=True, cwd=working_directory)

        to_return = ""

        if results.stdout:
            to_return += f'STDOUT: {results.stdout}\n'
        if results.stderr:
            to_return += f'STDERR: {results.stderr}\n'
        if results.returncode != 0:
            to_return += f'Process exited with code {results.returncode}'
        
        if not results.stdout and not results.stderr:
            to_return += f'No output produced.'

        return to_return

    except Exception as e:
        return f"Error: executing Python file: {e}"