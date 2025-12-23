from typing import List, Dict

class SearchTool:
    def __init__(self, max_findings: int = 4):
        self.max_findings = max_findings

    def build_cntext(self, query:str, results: List[Dict] -> str):
        """
        convert Tavily Raw results into a structured web search contxt
        for LLM
        """

        if not results:
            return self._empty_context(query)

        #sort by relavance score
        sorted_results = sorted(
            results,
            key= lambda r: r.get("score", 0),
            reverse = True
        )