from tavily_client import TavilySearchClient
from search_tool import SearchTool
from llm_short_answer import ShortAnswerLLM


query = "What is the EU AI Act?"

# Web search
tavily = TavilySearchClient()
results = tavily.search(query)

# Build context
search_tool = SearchTool()
context = search_tool.build_context(query, results)

# Short answer
llm = ShortAnswerLLM()
answer = llm.answer(query, context)

print("\nSHORT ANSWER:\n")
print(answer)
