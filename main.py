import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import *

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file, 
        schema_run_python_file
    ]
)

def main():
    print("Hello from ai-agent!\n")
    
    if len(sys.argv) < 2:
        print("Please enter a prompt.")
        sys.exit(1)
    else:
        verbose = "--verbose" in sys.argv
        user_prompt = sys.argv[1]
        messages = [
                types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ] 
        response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
        )
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
                    
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        
        if not response.candidates or not response.candidates[0].content.parts:
            print("No valid response from the model.")
            sys.exit(1)

        part = response.candidates[0].content.parts[0]

        if not hasattr(part, "function_call") or not part.function_call:
            if hasattr(part, "text") and part.text:
                print(part.text)
            else:
                print("No function call in the model's response.")
            sys.exit(1)
        
        function_call_part = part.function_call
        function_call_result = call_function(function_call_part, verbose=verbose)

        if not function_call_result.parts or not hasattr(function_call_result.parts[0], "function_response"):
            raise ValueError("Invalid function call result: No function response found.")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

if __name__ == "__main__":
    main()
