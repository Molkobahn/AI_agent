import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        try:
            os.makedirs(os.path.dirname(os.path.abspath(full_path)), exist_ok=True)
        except Exception as e:
            return f'Error creating file "{file_path}": {e}'
    
    try:
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to "{file_path}": {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write provided content to file in the working directory. Create file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)