import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


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
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
res = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

print(res.text)
