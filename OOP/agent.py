import json                                            # for terminal acess
import typing                                                   # type hints
from openai import OpenAI 
from tool_registry import ToolRegistry

from tools import (
    run_shell_command,
    read_file,
    write_file,
    system_info
)

from schemas import tool_definitions




client = OpenAI(api_key="your api key")
#-----------------------------------------------------------------------------------------------------------------
#Tool Registry 
#----------------------------------------------------------------------------------------------------------------

TOOLS = {                                                         #Dictionary to map real python object for the tools
    "run_shell_command": run_shell_command,
    "read_file": read_file,
    "write_file": write_file,
    "system_info": system_info
}

tool_registry = ToolRegistry(TOOLS)


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

                tool_result = tool_registry.execute(tool_name, tool_args)                  #execute the tool

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
