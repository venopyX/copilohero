# tools/websearch.py

import logging
from googlesearch import search, SearchResult
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class WebSearchTool(BaseTool):
    """
    Performs a Google search and retrieves top results based on the query.
    """

    def invoke(self, input: dict) -> dict:
        query = input.get("query")
        num_results = input.get("num_results", 5)

        if not query:
            return {"error": "Query parameter is required."}

        try:
            # Perform Google search using advanced mode to get title, url, and description
            search_results = search(query, num_results=num_results, sleep_interval=2, advanced=True)

            # Format the search results
            formatted_results = []
            for result in search_results:
                # Check if result is a SearchResult object
                if isinstance(result, SearchResult):
                    formatted_results.append({
                        "title": result.title if result.title else "No Title",
                        "url": result.url,
                        "description": result.description if result.description else "No Description"
                    })
                else:
                    # Handle the case where only a URL is returned
                    formatted_results.append({
                        "title": "No Title",
                        "url": result,
                        "description": "No Description"
                    })

            return {"results": formatted_results}

        except Exception as e:
            logger.error(f"Error performing Google search: {str(e)}")
            return {"error": f"Exception during search: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the web search tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to perform for up-to-date infos and future updates."
                },
                "num_results": {
                    "type": "integer",
                    "description": "The number of search results to retrieve.",
                    "default": 5
                }
            },
            "required": ["query"]
        }
