from tavily_client import TavilySearchClient
from search_tool import SearchTool

client = TavilySearchClient()
search_tool = SearchTool()

query = "What is the EU AI Act?"
results = client.search(query)

context = search_tool.build_context(query, results)
print(context)
