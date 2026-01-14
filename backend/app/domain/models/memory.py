import logging
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.domain.models.tool_result import ToolResult


logger = logging.getLogger(__name__)

class Memory(BaseModel):
    """
    Memory class, defining the basic behavior of memory
    """
    messages: List[Dict[str, Any]] = []

    def get_message_role(self, message: Dict[str, Any]) -> str:
        """Get the role of the message"""
        return message.get("role")

    def add_message(self, message: Dict[str, Any]) -> None:
        """Add message to memory"""
        self.messages.append(message)
    
    def add_messages(self, messages: List[Dict[str, Any]]) -> None:
        """Add messages to memory"""
        self.messages.extend(messages)

    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all message history"""
        return self.messages
    
    def get_last_message(self) -> Optional[Dict[str, Any]]:
        """Get the last message"""
        if len(self.messages) > 0:  
            return self.messages[-1]
        return None
    
    def roll_back(self) -> None:
        """Roll back memory"""
        self.messages = self.messages[:-1]
    
    def compact(self) -> None:
        """Compact memory"""
        for message in self.messages:
            if message.get("role") == "tool":
                if message.get("function_name") in ["browser_view", "browser_navigate"]:
                    message["content"] = ToolResult(success=True, data='(removed)').model_dump_json()
                    logger.debug(f"Removed tool result from memory: {message['function_name']}")

    @property
    def empty(self) -> bool:
        """Check if memory is empty"""
        return len(self.messages) == 0
