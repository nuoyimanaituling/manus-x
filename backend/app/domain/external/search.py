from typing import Optional, Protocol
from app.domain.models.tool_result import ToolResult
from app.domain.models.search import SearchResults

class SearchEngine(Protocol):
    """Search engine service gateway interface"""
    
    async def search(
        self, 
        query: str, 
        date_range: Optional[str] = None
    ) -> ToolResult[SearchResults]:
        """Search webpages using search engine
        
        Args:
            query: Search query, Google search style, using 3-5 keywords
            date_range: (Optional) Time range filter for search results
            
        Returns:
            Search results
        """
        ... 