import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in you function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
res = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

if res.function_calls != None:
    for func in res.function_calls:
        print(f"Calling function: {func.name}({func.args})")
else:
    print(res.text)
