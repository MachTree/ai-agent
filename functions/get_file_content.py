import os

from google.genai import types

from config import MAX_CHARACTER_LIMIT


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns the content (at most {MAX_CHARACTER_LIMIT} characters) of a specified file, relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be read, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        if os.path.commonpath([abs_path, target_file]) != abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            file_content = f.read(MAX_CHARACTER_LIMIT)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARACTER_LIMIT} characters]'
        return file_content
    except Exception as err:
        return f'Error reading file "{file_path}": {err}'

    