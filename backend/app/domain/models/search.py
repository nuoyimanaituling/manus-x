from pydantic import BaseModel, Field
from typing import List, Optional


class SearchResultItem(BaseModel):
    """Single search result item"""
    title: str = Field(..., description="Title of the search result")
    link: str = Field(..., description="URL link of the search result")
    snippet: str = Field(default="", description="Snippet or description of the search result")


class SearchResults(BaseModel):
    """Complete search results data structure"""
    query: str = Field(..., description="Original search query")
    date_range: Optional[str] = Field(default=None, description="Date range filter applied")
    total_results: int = Field(default=0, description="Total results count")
    results: List[SearchResultItem] = Field(default_factory=list, description="List of search results")
