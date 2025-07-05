import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = "--verbose" in sys.argv
    user_prompt = sys.argv[1]
    if not user_prompt:
        print("Query needed")
        sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in you function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
 

    for _ in range(20):
        res = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
        
        for candidate in res.candidates:
            messages.append(candidate.content)
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

        if res.function_calls != None:
            for function_call_part in res.function_calls:
                result = call_function(function_call_part, verbose)
                if not result.parts[0].function_response.response:
                    raise ValueError("No value returned from function call")
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")
                messages.append(result)
        else:
            print(res.text)
            break

main()
