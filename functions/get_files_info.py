import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
            name = "get_files_info",
            description = "Lists files in the specified directory along with their sizes, constrained to the working directory.",
            parameters = types.Schema(
                type = types.Type.OBJECT,
                properties = {
                    "directory": types.Schema(
                        type = types.Type.STRING,
                        description = "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself",
                        ),
                    },
                ),
            )

def get_files_info(working_directory, directory="."):
    abs_target = os.path.abspath(os.path.join(working_directory, directory))
    abs_work = os.path.abspath(working_directory)
    prefix = abs_work + os.path.sep
    

    if not (abs_target == abs_work or abs_target.startswith(prefix)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'

    try:
        entries = os.listdir(abs_target)
        lines = []

        for entry in entries: 
            full_path = os.path.join(abs_target, entry)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"

