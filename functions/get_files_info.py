import os

class DirectoryContent:
    def __init__(self, name, size, is_dir):
        self.name = name
        self.size = size
        self.is_dir = is_dir


def get_files_info(working_directory, directory=None):
    
    if not directory:
        directory = "."

    wd_abs = os.path.abspath(working_directory)
    dir_abs = os.path.abspath(os.path.join(working_directory, directory))

    if not (dir_abs == wd_abs or dir_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(dir_abs):
        return f'Error: "{directory}" is not a directory'
    
    try:
        elements_list = []
        for element in os.listdir(dir_abs):
            new_element = DirectoryContent(
                name=str(element),
                size=os.path.getsize(os.path.join(dir_abs, element)),
                is_dir=os.path.isdir(os.path.join(dir_abs, element))
            )
            elements_list.append(new_element)
    except Exception as e:
        return f"Error: {e}"
    
    final_string = f""
    for elem in elements_list:
        final_string += f"- {elem.name}: file_size={elem.size}, is_dir={elem.is_dir}\n"
        
    return final_string.rstrip()