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
