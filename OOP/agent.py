import json
import subprocess                                               # for terminal acess
import typing                                                   # type hints
from openai import OpenAI 

client = OpenAI(api_key="your api")                                                # OpenAI client, reads api from .env


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



def write_file(path:str, content:str) -> str:                   # write content on file and return string
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

tool_definitions = [
    {
        "type": "function",
        "name": "run_shell_command",
        "description": "Run a shell command on the system",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string"}
            },
            "required": ["command"]
        }
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "Read a text file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write content to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "type": "function",
        "name": "system_info",
        "description": "Get system information",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]



#------------------------------------------------------------
#Agent Loop - the real meat
#------------------------------------------------------------

def run_agent(user_input:str):
    response = client.responses.create(
        model = "gpt-4.1-mini",
        tools = tool_definitions,
        input = [
            {
                "role": "system",
                "content": (
                    "You are autonomous terminal AI agent. "
                    "You can inspect system, run commands, read/write files. "
                    "Think step by step, use tools when needed"
                )
            },
            { "role": "user", "content": user_input }
        ]
    )

    while True:                                                                     #need clarifications
        outputs = response.output

        tool_calls = [o for o in outputs if o.type == "function_call"]

        if tool_calls:                                                      #if model wants to call a tool
            for tool_call in tool_calls:
                tool_name = tool_call.name
                tool_args = json.loads(tool_call.arguments or "{}")          #return json tool arguments as python dict

                print(f"\n󰘧 TOOL CALL -> {tool_name}({tool_args})")

                tool_result = TOOLS[tool_name](**tool_args)                  #execute the tool

                # IMPORTANT: Responses API does NOT accept role="tool"
                # Tool output must be sent as function_call_output
                response = client.responses.create(
                    model = "gpt-4.1-mini",
                    tools = tool_definitions,
                    previous_response_id = response.id,
                    input = [
                        {
                            "type": "function_call_output",
                            "call_id": tool_call.call_id,
                            "output": str(tool_result)
                        }
                    ]
                )
        else:
            print("\n󰊠 AGENT RESPONSE:\n")
            print(response.output_text)
            break




#Entry Point

if __name__ == "__main__":
    print("󰚩 Terminal AI Ops Agent")
    print("Type your request (or 'exit')\n")

    while True:
        user_input = input("> ")
        if user_input.lower() in {"exit", "quit"}:
            break
        run_agent(user_input)
