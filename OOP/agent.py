import json
import subprocess                                               # for terminal acess
import typing                                                   # type hints
from openai import OpenAI 

client = OpenAI                                                 # OpenAI client, reads api from .env


#-----------------------------------------------------------------------------------------------------------------------------------
#TOOLS
#-----------------------------------------------------------------------------------------------------------------------------------


def run_shell_command(command:str) -> str:
    """ Run a shell command safely"""
    try:
        result = subprocess.run(
            command,
            shell = True,                                        # runs shell,convinent but security risk
            capture_output = True,                               # capture strout/strerr instead of pointing to screen
            text = True,                                         # returns text string instead of raw bites
            timeout = 10
        )
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)


def read_file(path:str) -> str:                                  # reads file content and returns it as string
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)



def write_file(path:str, content:str) -> astr:
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"File written to {path}"
    except Exception as e:
        return str(e)



def system_info() -> str:
    return {
        "os": run_shell_command("uname -a"),
        "disk": run_shell_command("df -h"),
        "memory": run_shell_command("free -h")
    }
