# ------------------------------------------------------------
# Prompt builder for LONG, STRUCTURED, GROUNDED answers
# This prompt forces the LLM to return JSON ONLY
# ------------------------------------------------------------


def build_long_answer_prompt(query: str, web_context: str) -> str:
    """
    Builds a strict prompt that forces the LLM to return
    a structured JSON object suitable for text rendering.
    """ 

    return f"""

You are a research assistant.

You must follow these rules strictly:

Rules: 
- Use only the information from WEB_SEARCH_CONTEXT
- Do NOT use prior knowledge
- Do NOT hallucinate
- Do NOT include opinions
- Do NOT inlcude markdown
- Do NOT include explanation outside JSON
- Output must be valid JSON ONLY
- Do NOT wrap JSON in backticks
- Do NOT add any text before or after JSON

Your task:
Analyze the web search context and produce a structured research brief.

------------------------------------------------------
WEB_SEARCH_CONTEXT
------------------------------------------------------
{web_context}
------------------------------------------------------

Return JSON in EXACTLY this struture:

{{
  "title": "<short research title>",
  "query": "{query}",
  "summary": "<3–5 sentence neutral summary>",
  "sections": [
    {{
      "heading": "<section heading>",
      "points": [
        "<bullet point>",
        "<bullet point>"
      ]
    }},
    {{
      "heading": "<section heading>",
      "subsections": [
        {{
          "label": "<subcategory name>",
          "points": [
            "<bullet point>",
            "<bullet point>"
          ]
        }}
      ]
    }}
  ],
  "sources": [
    {{
      "title": "<source title>",
      "url": "<source url>"
    }}
  ]
}}

IMPORTANT CONSTRAINTS:
- Each section must have either "points" OR "subsections", never both
- Bullet points must be short and factual
- Minimum 3 sections total
- Include a section named "Practical Impact"
- Sources must come from WEB_SEARCH_CONTEXT only

Return ONLY the JSON.
"""
