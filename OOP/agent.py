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



def write_file(path:str, content:str) -> astr:                   # write content on file and return string
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"File written to {path}"
    except Exception as e:
        return str(e)



def system_info() -> str:                                         # pre-defined systeminfo using zsh commands
    return {
        "os": run_shell_command("uname -a"),
        "disk": run_shell_command("df -h"),
        "memory": run_shell_command("free -h")
    }


#-----------------------------------------------------------------------------------------------------------------
#Tool Registry 
#----------------------------------------------------------------------------------------------------------------

TOOLS = {                                                         #Dictionary to map real python object for the tools
    "run_shell_command": run_shell_command,
    "read_file": read_file,
    "write_file": write_file,
    "system_info": system_info

}



#----------------------------------------------
#Tool schema - each schema is in OpenAI tool/function format
#----------------------------------------------

tool_definitions= [
    {
        "type": "funtion",                                                       #callable funntion
        "function": {                                       
            "name": "run_shell_command",                                         #must exactly match the key in tools
            "description": " Run a shell command on the system",                 #model uses this to decided whether to use this tool
            "parameters": {                                                      # JSON schema that tells model what arguments to provide
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]                                          #model must include command   
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "system_info",
            "description": "Get system information",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]