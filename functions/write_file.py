import os

from google.genai import types


def _write_file(working_directory, file_path, content):
    try:
        working_dir_path = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        if os.path.isdir(full_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        valid_target_path = (
            os.path.commonpath([working_dir_path, full_file_path]) == working_dir_path
        )
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Make sure that all parent directories of the file_path exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        f = open(full_file_path, "w")
        f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


def write_file(file_path: str, content: str) -> str:
    """Writes content to a file relative to the working directory

    Args:
        file_path: Path of file to write content to, relative to the working directory
        content: Content to write to the file

    Returns:
        A success message with the number of characters written, or an error message.
    """

    working_directory = "./calculator"
    return _write_file(working_directory, file_path, content)


schema_write_file_genai = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a given file name relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
