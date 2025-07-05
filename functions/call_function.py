from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types


def call_function(function_call_part, verbose=False):    
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_call_part.args["working_directory"] = "./calculator"
    
    get_file_content_dict = {
        "working_directory": "",
        "file_path": "",
        }
    if function_call_part.name == "get_file_content":
        get_file_content_dict["working_directory"] = function_call_part.args["working_directory"]
        get_file_content_dict["file_path"] = function_call_part.args["file_path"]
    
    get_files_info_dict = {
        "working_directory": "",
        "directory": "",
    }
    if function_call_part.name == "get_files_info":
        get_files_info_dict["working_directory"] = function_call_part.args["working_directory"]
        if "directory" in function_call_part.args:
            get_files_info_dict["directory"] = function_call_part.args["directory"]
    
    run_python_file_dict = {
        "working_directory": "",
        "file_path": "",
    }
    if function_call_part.name == "run_python_file":
        run_python_file_dict["working_directory"] = function_call_part.args["working_directory"]
        run_python_file_dict["file_path"] = function_call_part.args["file_path"]

    write_file_dict = {
        "working_directory": "",
        "file_path": "",
        "content": "",
    }
    if function_call_part.name == "write_file":
        write_file_dict["working_directory"] = function_call_part.args["working_directory"]
        write_file_dict["file_path"] = function_call_part.args["file_path"]
        write_file_dict["content"] = function_call_part.args["content"]
    functions = {
    "get_file_content": get_file_content(**get_file_content_dict),
    "get_files_info": get_files_info(**get_files_info_dict),
    "run_python_file": run_python_file(**run_python_file_dict),
    "write_file": write_file(**write_file_dict),
    }

    result = functions[function_name]
    if not result:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )