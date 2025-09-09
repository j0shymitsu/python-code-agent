import sys, os

def write_file(working_directory, file_path, content):
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)
    abs_dir = os.path.dirname(abs_target)

    if not (abs_target == abs_work or abs_target.startswith(abs_work + os.path.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(abs_dir, exist_ok=True)
        if os.path.isdir(abs_target):
            return f'Error: {abs_target} is directory'
        with open(abs_target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
    