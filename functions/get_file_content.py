import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_path = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        valid_target_path = (
            os.path.commonpath([working_dir_path, full_file_path]) == working_dir_path
        )
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        f = open(full_file_path, "r")
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content

    except Exception as e:
        return f"Error: {e}"
