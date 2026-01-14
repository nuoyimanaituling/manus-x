from typing import Any, Protocol, Tuple, Optional

class MessageQueue(Protocol):
    """Message queue interface for agent communication"""
    
    async def put(self, message: Any) -> str:
        """Put a message into the queue
        
        Returns:
            str: Message ID
        """
        ...
    
    async def get(self, start_id: Optional[str] = None, block_ms: Optional[int] = None) -> Tuple[str, Any]:
        """Get a message from the queue
        
        Args:
            start_id: Message ID to start reading from, defaults to "0" meaning from the earliest message
            block_ms: Block time in milliseconds, defaults to None meaning no blocking
            
        Returns:
            Tuple[str, Any]: (Message ID, Message content), returns (None, None) if no message
        """
        ...
    
    async def pop(self) -> Tuple[str, Any]:
        """Get and remove the first message from the queue
        
        Returns:
            Tuple[str, Any]: (Message ID, Message content), returns (None, None) if queue is empty
        """
        ...
    
    async def clear(self) -> None:
        """Clear all messages from the queue"""
        ...
    
    async def is_empty(self) -> bool:
        """Check if the queue is empty"""
        ...
    
    async def size(self) -> int:
        """Get the current size of the queue"""
        ...

    async def delete_message(self, message_id: str) -> bool:
        """Delete a specific message from the queue
        
        Args:
            message_id: ID of the message to delete
            
        Returns:
            bool: True if message was deleted successfully, False otherwise
        """
        ... 
