import json 
from openai import OpenAI 

from tavily_client import TavilySearchClient
from search_tool import SearchTool
from long_answer_prompt import build_long_answer_prompt

# ------------------------------------------------------------
# Setup clients
# ------------------------------------------------------------

client = OpenAI()
tavily = TavilySearchClient()
search_tool = SearchTool(max_findings=4)

# ------------------------------------------------------------
# Test query
# ------------------------------------------------------------

query = "What is the EU AI Act"


# ------------------------------------------------------------
# 1️⃣ Run Tavily search
# ------------------------------------------------------------

results = tavily.search(query)

web_context = search_tool.build_context(
    query = query,
    results = results
)

print("\n--- WEB SEARCH CONTEXT ---\n")
print(web_context)

# ------------------------------------------------------------
# 2️⃣ Build long-answer prompt
# ------------------------------------------------------------

prompt = build_long_answer_prompt(
    query=query,
    web_context=web_context
)

# ------------------------------------------------------------
# 3️⃣ Call LLM
# ------------------------------------------------------------

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

# ------------------------------------------------------------
# 4️⃣ Parse + validate JSON
# ------------------------------------------------------------

print("\n--- RAW LLM OUTPUT ---\n")
print(response.output_text)

try:
    data =json.loads(response.output_text)
except json.JSONDecoderError as e:
    raise RuntimeError("❌ LLM output is NOT valid JSON") from e
    


# ------------------------------------------------------------
# 5️⃣ Safety checks
# ------------------------------------------------------------
required_keys = {"title", "query", "summary", "sections", "sources"}
assert required_keys.issubset(data.keys()), "❌ Missing required keys"

assert isinstance(data["sections"], list) and data["sections"], "❌ Sections invalid"

assert any(
    section.get("heading", "").lower() == "practical impact"
    for section in data["sections"]
), "❌ Missing 'Practical Impact' section"


print("\n✅ JSON STRUCTURE VALID")
print("✅ Required keys present")
print("✅ Practical Impact section found")

print("\n--- PARSED JSON (pretty) ---\n")
print(json.dumps(data, indent=2))