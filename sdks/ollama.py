import sys

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

    response: ChatResponse = None

    for _ in range(20):
        response = chat(
            model="custom_model",
            messages=messages,
            tools=list(available_functions.values()),
            think=True
        )

        messages.append(response.message)

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
                    tool = ToolCall(name=tc.function.name, args=tc.function.arguments)
                    response_function_calls.append(tool)
                    function_result = call_function(tool, verbose)
                    if function_result["content"] == None:
                        raise Exception("Error: tool call content not found")

                    if verbose:
                        print(f"-> {function_result['content']}")

                    messages.append(function_result)

        else:
            break

    if response.message.content == "":
        print("Error: Model did not generate final response")
        sys.exit(1)



    return (
        prompt_token_count,
        response_token_count,
        response.message.content,
        response_function_calls,
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
            "content": str({"error": f"Unknown function: {function_name}"}),
        }

    args = dict(function_call.args) if function_call.args else {}

    # Call function
    function_result = available_functions[function_name](**args)

    return {
        "role": "tool",
        "tool_name": function_name,
        "content": str({"result": function_result}),
    }
