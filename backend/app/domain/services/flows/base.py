from app.domain.models.event import BaseEvent
from app.domain.models.agent import Agent
from typing import AsyncGenerator
from abc import ABC, abstractmethod
from app.domain.repositories.agent_repository import AgentRepository

class BaseFlow(ABC):

    @abstractmethod
    def run(self) -> AsyncGenerator[BaseEvent, None]:
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass
