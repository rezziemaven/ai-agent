import sys

from google import genai
from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content_genai
from functions.get_files_info import get_files_info, schema_get_files_info_genai
from functions.run_python_file import run_python_file, schema_run_python_file_genai
from functions.write_file import schema_write_file_genai, write_file
from prompts import system_prompt

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info_genai,
        schema_get_file_content_genai,
        schema_write_file_genai,
        schema_run_python_file_genai,
    ],
)


def use_genai_sdk(api_key, prompt, verbose=False):
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    prompt_token_count = 0
    response_token_count = 0

    if response.usage_metadata != None:
        prompt_token_count = response.usage_metadata.prompt_token_count
        response_token_count = response.usage_metadata.candidates_token_count

    function_results = []
    function_call_result = None
    # print(response.function_calls)
    if response.function_calls:
        function_call_result = call_function(
            response.function_calls[0], verbose=verbose
        )

        if function_call_result.parts == None:
            raise Exception("Error: function call should have a non-empty parts list")

        if function_call_result.parts[0].function_response == None:
            raise Exception("Error: no function response found")

        if function_call_result.parts[0].function_response.response == None:
            raise Exception("Error: no response found")

        function_results.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    if response.text == "":
        print("Error: Model did not generate final response")
        sys.exit(1)


def call_function(function_call, verbose=False):
    # print("function call:", function_call)
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args}")
    print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    # args["working_directory"] = "./calculator"

    # Call function
    function_result = function_map[function_name](**args)
    # function_result = function_map[function_name](*function_call.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
