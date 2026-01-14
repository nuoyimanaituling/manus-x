from pydantic import BaseModel
from typing import Any, Optional, TypeVar, Generic

T = TypeVar('T')

class ToolResult(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
