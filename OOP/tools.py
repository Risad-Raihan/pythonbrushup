import subprocess

def run_shell_command(command:str) -> str:
    """run a shell command safely"""
    try:
        result = subprocess.run(
            command,
            shell = True,
            capture_output = True,
            text = True,
            timeout = 10
        )
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)



def read_file(path:str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)



def write_file(path:str, content:str) -> str:
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"File written to {path}"
    except Exception as e:
        return str(e)



def system_info() -> str:
    return{
        "os": run_shell_command("uname -a"),
        "disk": run_shell_command("df -h"),
        "memory": run_shell_command("free -h")
    }