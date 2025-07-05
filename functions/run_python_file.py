import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a python file'
    
    try:
        result = subprocess.run(["python", abs_file_path], capture_output=True, text=True, timeout=30, cwd=abs_working_directory)
        STDOUT = f'STDOUT: {result.stdout}'
        STDERR = f'STDERR: {result.stderr}'
        output = STDOUT + STDERR

        if result.returncode != 0:
            output += f'Process exited withcode {result.returncode}'

        if STDOUT == "" and STDERR == "":
            return f'No output produced'

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"    


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a the Python file at the given file path. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run.",
            ),
        },
        required=["file_path"],
    ),
)