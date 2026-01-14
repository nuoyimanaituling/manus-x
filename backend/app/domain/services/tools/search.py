from typing import Optional
from app.domain.external.search import SearchEngine
from app.domain.services.tools.base import tool, BaseTool
from app.domain.models.tool_result import ToolResult

class SearchTool(BaseTool):
    """Search tool class, providing search engine interaction functions"""

    name: str = "search"
    
    def __init__(self, search_engine: SearchEngine):
        """Initialize search tool class
        
        Args:
            search_engine: Search engine service
        """
        super().__init__()
        self.search_engine = search_engine
    
    @tool(
        name="info_search_web",
        description="Search web pages using search engine. Use for obtaining latest information or finding references.",
        parameters={
            "query": {
                "type": "string",
                "description": "Search query in Google search style, using 3-5 keywords."
            },
            "date_range": {
                "type": "string",
                "enum": ["all", "past_hour", "past_day", "past_week", "past_month", "past_year"],
                "description": "(Optional) Time range filter for search results."
            }
        },
        required=["query"]
    )
    async def info_search_web(
        self,
        query: str,
        date_range: Optional[str] = None
    ) -> ToolResult:
        """Search webpages using search engine
        
        Args:
            query: Search query, Google search style, using 3-5 keywords
            date_range: (Optional) Time range filter for search results
            
        Returns:
            Search results
        """
        return await self.search_engine.search(query, date_range) 