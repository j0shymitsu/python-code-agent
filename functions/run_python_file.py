import sys, os, subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)

    if not (abs_target == abs_work or abs_target.startswith(abs_work + os.path.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not abs_target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    if not os.path.exists(abs_target):
        return f'Error: File "{file_path}" not found.'
    
    
    
    try:
        cmd = [sys.executable, file_path, *args]
        output = subprocess.run(cmd, cwd=abs_work, timeout=30, capture_output=True, text=True)

        stdout = output.stdout or ""
        stderr = output.stderr or ""

        if output.returncode == 0 and not stdout and not stderr:
            return f'No output produced.'
        
        parts = [f"STDOUT: {stdout}", f"STDERR: {stderr}"]

        if output.returncode != 0:
            parts.append(f"Process exited with code {output.returncode}")
        return "\n".join(parts)
    
    except Exception as e:
        f"Error: executing Python file: {e}"

