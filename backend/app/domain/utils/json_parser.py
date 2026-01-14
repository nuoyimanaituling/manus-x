from typing import Protocol, Optional, Any, Union, Dict, List

class JsonParser(Protocol):
    """Json parser interface"""
    
    async def parse(self, text: str, default_value: Optional[Any] = None) -> Union[Dict, List, Any]:
        """
        Parse LLM output string to JSON using multiple strategies.
        Falls back to LLM parsing if local strategies fail.
        
        Args:
            text: The raw string output from LLM
            default_value: Default value to return if parsing fails
            
        Returns:
            Parsed JSON object (dict, list, or other JSON-serializable type)
            
        Raises:
            ValueError: If all parsing strategies fail and no default value provided
        """
