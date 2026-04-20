import os
import subprocess

from google.genai import types


def _run_python_file(working_directory, file_path, args=None):

    try:
        working_dir_path = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        if not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        valid_target_path = (
            os.path.commonpath([working_dir_path, full_file_path]) == working_dir_path
        )
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        command = ["python", full_file_path]
        if args != None:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_dir_path, capture_output=True, text=True, timeout=30
        )

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if result.stdout == "" and result.stderr == "":
            output += "No output produced"
        if result.stdout != "":
            output += f"STDOUT: {result.stdout}\n"
        if result.stderr != "":
            output += f"STDERR: {result.stderr}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


def run_python_file(file_path: str, args=None) -> str:
    """Executes a python file within the working directory

    Args:
        file_path: Python file to execute, relative to the working directory
        args: List of arguments to pass to the file

    Returns:
        A message with the content from STDOUT or STDERR if the execution was successful, or an error message.
    """

    working_directory = "./calculator"
    return _run_python_file(working_directory, file_path, args)


schema_run_python_file_genai = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the file",
            ),
        },
        required=["file_path"],
    ),
)
