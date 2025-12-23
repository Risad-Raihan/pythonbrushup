from tavily_client import TavilySearchClient
from search_tool import SearchTool
from llm_short_answer import ShortAnswerLLM
from ui import (
    render_header,
    prompt_user_question,
    render_thinking,
    render_short_answer,
    ask_decision,
    ask_next_action
)

#------------------------------------------------------------
# Main Agent Loop
#------------------------------------------------------------

def run_agent():
    tavily = TavilySearchClient()
    search_tool = SearchTool()
    llm = ShortAnswerLLM()

    render_header()

    while True:
        #ask question
        query = prompt_user_question()
        if not query:
            continue

        #web search + context
        render_thinking()
        results = tavily.search(query)
        context = search_tool.build_context(query, results)

        #short answer
        answer = llm.answer(query, context)
        render_short_answer(answer)

        #Decision gate
        choice = ask_decision()
        if choice == "m":
            print("\n󰒓 Long answer generation coming next...\n")

        #next action
        next_action = ask_next_action()
        if next_action == "q":
            print("\n👋 Goodbye.\n")
            break



if __name__ == "__main__":
    run_agent()