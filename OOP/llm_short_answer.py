from openai import OpenAI



class ShortAnswerLLM:
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.client = OpenAI()
        self.model = model

        self.system_prompt = (
            "You are a research assistant.\n\n"
            "Use the provided web search context as your only source of truth.\n"
            "Answer the user's question in no more than 50 words.\n\n"
            "Rules:\n"
            "- Be direct and factual\n"
            "- No markdown, no bullet points\n"
            "- No introductions or conclusions\n"
            "- If the information is incomplete, say so briefly"
        )


    def answer(self, query: str, web_context: str) -> str:
        response = self.client.responses.create(
            model = self.model,
            input=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Question:\n{query}\n\n"
                        f"{web_context}"
                    )
                }
            ],
        )

        return response.output_text.strip()