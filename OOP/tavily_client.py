import os
from dotenv import load_dotenv
from typing import List, Dict
from tavily import TavilyClient

load_dotenv()

class TavilySearchClient:
    def __init__(self, api_key: str | None = None):
        #loaded from .emv
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

        if not self.api_key:
            raise ValueError("API not found on env")

        self.client =  TavilyClient(api_key=self.api_key)

    
    def search(
        self,
        query:str,
        max_results: int = 4,
        search_depth:str = "basic",
        topic: str = "general"
    ) -> List[Dict]:
        """
        tavily web serach and return raw result:
        - title
        - url
        - content
        - score
        """

        response = self.client.search(
            query = query,
            max_results = max_results,
            search_depth = search_depth,
            topic = topic,
            include_answer =  False,
            include_raw_content = False
        )

        return response.get("results", [])