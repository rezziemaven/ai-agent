from dataclasses import dataclass

from ollama import ChatResponse, chat, create

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from prompts import system_prompt

available_functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


@dataclass
class ToolCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


def use_ollama_sdk(prompt, verbose=False):
    messages = [{"role": "user", "content": prompt}]
    create(model="custom_model", from_="minimax-m2.5:cloud", system=system_prompt)

    prompt_token_count = 0
    response_token_count = 0
    response_function_calls = []

    if response != None:
        prompt_token_count = response.prompt_eval_count
        response_token_count = response.eval_count

    if response.message.tool_calls:
        for tc in response.message.tool_calls:
            if tc.function.name in available_functions:
                response_function_calls.append(
                    ToolCall(name=tc.function.name, args=tc.function.arguments)
                )

    function_results = []
    function_call_result = None
    # print(response.function_calls)
    if len(response_function_calls) != 0:
        function_call_result = call_function(
            response_function_calls[0], verbose=verbose
        )

        if function_call_result["content"] == None:
            raise Exception("Error: tool call content not found")

        function_results.append(function_call_result)

        if verbose:
            print(f"-> {function_call_result['content']}")

    return (
        prompt_token_count,
        response_token_count,
        response.message.content,
        function_results,
    )


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args}")
    print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""

    if function_name not in available_functions:
        return {
            "role": "tool",
            "tool_name": function_name,
            "content": {"error": f"Unknown function: {function_name}"},
        }

    args = dict(function_call.args) if function_call.args else {}

    # Call function
    function_result = available_functions[function_name](**args)

    return {
        "role": "tool",
        "tool_name": function_name,
        "content": {"result": function_result},
    }
