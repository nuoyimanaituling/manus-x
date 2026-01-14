from typing import Optional, Any
from pydantic import BaseModel, Field

# Unified response model
class Response(BaseModel):
    """Generic response model for API interface return results"""
    success: bool = Field(True, description="Whether the operation was successful")
    message: Optional[str] = Field("Operation successful", description="Operation result message")
    data: Optional[Any] = Field(None, description="Data returned from the operation")

    # Shortcut method to create error response
    @classmethod
    def error(cls, message: str, data: Any = None) -> "Response":
        """Create an error response instance"""
        return cls(success=False, message=message, data=data) 