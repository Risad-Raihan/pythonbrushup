class ToolRegistry:
    def __init__(self, tools: dict):
        #tools = {"tool_name: callable"}
        self.tools = tools

    
    def execute(self, tool_name: str, tool_args:dict) -> str:
        if tool_name not in self.tools:
            return f"Unknown tool: {tool_name}"

        try:
            return self.tools[tool_name](**tool_args)
        except Exception as e:
            return str(e)



            