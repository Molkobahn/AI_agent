import os

def get_files_info(working_directory, directory=None):
    dir_path = os.path.join(working_directory, directory)
    
    if not os.path.abspath(dir_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory'
    print(f"The file path: {dir_path}")
    file_list = os.listdir(dir_path)
    res = f""
    for file in file_list:
        file_path = os.path.join(dir_path, file)
        if os.path.isdir(file_path):
            res += f"- {file}: file_size=92, is_dir={os.path.isdir(file_path)}"
        elif os.path.isfile(file_path):
            res += f"- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}\n"
    return res