#------------------------------------------------------------
#Response Parser - interprets OpenAI Responses API output
#------------------------------------------------------------


class ResponseParser:
    def __init__(self, response):
        self.response = response
        self.outputs = response.output

    def get_tool_calls(self):
        #return list of function call items
        return [o for o in self.outputs if o.type == "function_call"]

    def has_tool_calls(self) -> bool:
        return len(self.get_tool_calls()) > 0

    def get_text(self) -> str:
        #accessor for final text
        return self.response.output_text
