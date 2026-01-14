from typing import Optional, List, Protocol
from app.domain.models.agent import Agent
from app.domain.models.plan import Plan
from app.domain.models.memory import Memory

class AgentRepository(Protocol):
    """Repository interface for Agent aggregate"""
    
    async def save(self, agent: Agent) -> None:
        """Save or update an agent"""
        ...
    
    async def find_by_id(self, agent_id: str) -> Optional[Agent]:
        """Find an agent by its ID"""
        ...
    
    async def add_memory(self, agent_id: str,
                        name: str,
                        memory: Memory) -> None:
        """Add or update a memory for an agent"""
        ...

    async def get_memory(self, agent_id: str, name: str) -> Memory:
        """Get memory by name from agent, create if not exists"""
        ...

    async def save_memory(self, agent_id: str, name: str, memory: Memory) -> None:
        """Update the messages of a memory"""
        ... 