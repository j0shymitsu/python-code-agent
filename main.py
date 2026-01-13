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
    verbose = False
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    args = []
    print('Hello from ai-agent!\n')
    args = []

    if len(sys.argv) >= 2:
        verbose = "--verbose" in sys.argv
        for arg in sys.argv[1:]:
            if not arg.startswith("--"):
                args.append(arg)

    if args:
        user_prompt = " ".join(args)

    if not args:
        print('\nUsage: python main.py "[insert your prompt]" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')

    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    print(f'User prompt: {user_prompt}\n')
    print("Declared tools:", [fd.name for fd in available_functions.function_declarations])

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)])
    ]

    max_iterations = 20
    current_iteration = 0

    while True:
        current_iteration += 1

        if current_iteration > max_iterations:
            print(f"Maximum iterations ({max_iterations}) reached.")
            sys.exit(1)

        try:
            response = generate_content(client, messages, verbose)

            if response.usage_metadata is None:
                raise RuntimeError("Failed API request.")

            for cand in response.candidates:
                messages.append(cand.content)

            if response.function_calls:
                function_responses = []

                for part in response.function_calls:
                    fr = call_function(part, verbose)
                    function_responses.append(fr.parts[0])

                messages.append(types.Content(role="user", parts=function_responses))
                continue

            if response.text:
                print(response.text)
                break

        except Exception as e:
            print(f"Error: {e}")
            # Fallback
            print("Prompt tokens: 0")
            print("Response tokens: 0")
            break


def generate_content(client, messages, verbose):
    
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config = types.GenerateContentConfig(
            tools = [available_functions], system_instruction=system_prompt
        ),
    )

    print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
    print("Response tokens: ", response.usage_metadata.candidates_token_count)

    return response


if __name__ == "__main__":
    main()
