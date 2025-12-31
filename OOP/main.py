import json
from openai import OpenAI

from tavily_client import TavilySearchClient
from search_tool import SearchTool
from llm_short_answer import ShortAnswerLLM
from long_answer_prompt import build_long_answer_prompt
from text_renderer import TextRenderer
from slugger import slugify

from ui import (
    render_header,
    prompt_user_question,
    render_thinking,
    render_short_answer,
    ask_decision,
    ask_next_action
)

# ------------------------------------------------------------
# OpenAI client
# ------------------------------------------------------------

client = OpenAI()


# ------------------------------------------------------------
# Main Agent Loop
# ------------------------------------------------------------

def run_agent():
    tavily = TavilySearchClient()
    search_tool = SearchTool()
    short_llm = ShortAnswerLLM()
    renderer = TextRenderer()

    render_header()

    while True:
        # --------------------------------------------------
        # Ask user question
        # --------------------------------------------------
        query = prompt_user_question()
        if not query:
            continue

        # --------------------------------------------------
        # Web search + context
        # --------------------------------------------------
        render_thinking()
        results = tavily.search(query)
        context = search_tool.build_context(query, results)

        # --------------------------------------------------
        # Short answer
        # --------------------------------------------------
        short_answer = short_llm.answer(query, context)
        render_short_answer(short_answer)

        # --------------------------------------------------
        # Decision gate
        # --------------------------------------------------
        choice = ask_decision()

        if choice == "m":
            print("\n󰒓 Generating full research brief...\n")

            # ------------------------------------------
            # Long-answer prompt
            # ------------------------------------------
            prompt = build_long_answer_prompt(
                query=query,
                web_context=context
            )

            # ------------------------------------------
            # Call LLM for structured JSON
            # ------------------------------------------
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            data = json.loads(response.output_text)

            # ------------------------------------------
            # Render styled text
            # ------------------------------------------
            report_text = renderer.render(data)

            # ------------------------------------------
            # Generate filename + save
            # ------------------------------------------
            filename = slugify(data["title"])

            with open(filename, "w") as f:
                f.write(report_text)

            print(f"\n✅ Full report saved as: {filename}\n")

        # --------------------------------------------------
        # Next action
        # --------------------------------------------------
        next_action = ask_next_action()
        if next_action == "q":
            print("\n👋 Goodbye.\n")
            break


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    run_agent()
