from tavily_client import TavilySearchClient

client = TavilySearchClient()
results = client.search("What is the EU AI Act?")
print(results[0].keys())
