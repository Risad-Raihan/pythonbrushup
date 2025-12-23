from typing import List, Dict

class SearchTool:
    def __init__(self, max_findings: int = 4):
        self.max_findings = max_findings

    def build_context(self, query:str, results: List[Dict]) -> str:
        """
        convert Tavily Raw results into a structured web search contxt
        for LLM
        """

        if not results:
            return self._empty_context(query)

        #sort by relavance score - descending
        sorted_results = sorted(
            results,
            key= lambda r: r.get("score", 0),
            reverse = True
        )

        #limit results to top N
        top_results = sorted_results[: self.max_findings]

        key_findings = []
        sources = []

        for idx, result in enumerate(top_results, start =1):
            content = self._clean_content(result.get("content", ""))

            if content:
                key_findings.append(f"{idx}, {content}")

            title = result.get("title", "unknown Source")
            url = result.get("url", "")
            sources.append(f"[{idx}] {title} - {url}")

        context = (
            "WEB_SEARCH_CONTEXT\n"
            "==================\n"
            f"Query:\n{query}\n\n"
            "Key Findings:\n"
            + "\n".join(key_findings)
            + "\n\nSources:\n"
            + "\n".join(sources)
        )

        return context



    def _clean_content(self, text: str) -> str:
        """
        clean and compress tavily content into a single factual sentence
        """

        if not text:
            return ""

        #whitespace
        cleaned = " ".join(text.split())

        #limit length to save token
        return cleaned[:300]



    def _empty_context(self, query: str) -> str:
        """
        fallback if no result found
        """

        return (

            "WEB_SEARCH_CONTEXT\n"
            "==================\n"
            f"Query:\n{query}\n\n"
            "Key Findings:\n"
            "No relevant web results were found.\n\n"
            "Sources:\n"
            "None"
        )