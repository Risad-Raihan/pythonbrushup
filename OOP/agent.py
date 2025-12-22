import json                                            # for terminal acess
import typing                                          # type hints

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI 

from tool_registry import ToolRegistry
from schemas import tool_definitions
from response_parser import ResponseParser

from tools import (
    run_shell_command,
    read_file,
    write_file,
    system_info
)

client = OpenAI()        #calling from .env, setting up client

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
#Agent Class - refactored agent logic
#------------------------------------------------------------

class TerminalAgent:                                             # new added line
    def __init__(self, client, tool_registry, tool_definitions): # new added line
        self.client = client                                     # new added line
        self.tool_registry = tool_registry                       # new added line
        self.tool_definitions = tool_definitions                 # new added line

    def run(self, user_input: str):                               # new added line
        response = self.client.responses.create(
            model = "gpt-4.1-mini",
            tools = self.tool_definitions,
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

        while True:                                              #need clarifications
            parser = ResponseParser(response)

            if parser.has_tool_calls():                           #if model wants to call a tool
                for tool_call in parser.get_tool_calls():
                    tool_name = tool_call.name
                    tool_args = json.loads(tool_call.arguments or "{}")
                    
                    print(f"\n󰘧 TOOL CALL -> {tool_name}({tool_args})")

                    tool_result = self.tool_registry.execute(     # new added line
                        tool_name,
                        tool_args
                    )

                    response = self.client.responses.create(
                        model = "gpt-4.1-mini",
                        tools = self.tool_definitions,
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
                print(parser.get_text())
                break


#------------------------------------------------------------
#Entry Point
#------------------------------------------------------------

if __name__ == "__main__":
    print("󰚩 Terminal AI Ops Agent")
    print("Type your request (or 'exit')\n")

    agent = TerminalAgent(                                       # new added line
        client=client,
        tool_registry=tool_registry,
        tool_definitions=tool_definitions
    )

    while True:
        user_input = input("> ")
        if user_input.lower() in {"exit", "quit"}:
            break
        agent.run(user_input)                                   # new added line
