from typing import Optional, Protocol, List
from datetime import datetime
from app.domain.models.scheduled_task import ScheduledTask, ScheduledTaskStatus
from app.domain.models.scheduled_task_execution import ScheduledTaskExecution


class ScheduledTaskRepository(Protocol):
    """Repository interface for ScheduledTask"""

    async def save(self, task: ScheduledTask) -> None:
        """Save or update a scheduled task"""
        ...

    async def find_by_id(self, task_id: str) -> Optional[ScheduledTask]:
        """Find a task by ID"""
        ...

    async def find_by_user_id(self, user_id: str) -> List[ScheduledTask]:
        """Find all tasks for a user"""
        ...

    async def find_by_id_and_user_id(self, task_id: str, user_id: str) -> Optional[ScheduledTask]:
        """Find a task by ID and user ID (for authorization)"""
        ...

    async def find_active_tasks(self) -> List[ScheduledTask]:
        """Find all active tasks"""
        ...

    async def find_due_tasks(self, before: datetime) -> List[ScheduledTask]:
        """Find tasks due to run before the given time"""
        ...

    async def update_next_run(self, task_id: str, next_run_at: datetime) -> None:
        """Update the next run time"""
        ...

    async def update_last_run(self, task_id: str, last_run_at: datetime, session_id: str) -> None:
        """Update last run info"""
        ...

    async def update_status(self, task_id: str, status: ScheduledTaskStatus) -> None:
        """Update task status"""
        ...

    async def increment_run_count(self, task_id: str) -> None:
        """Increment run count"""
        ...

    async def increment_failure_count(self, task_id: str) -> None:
        """Increment failure count"""
        ...

    async def reset_failure_count(self, task_id: str) -> None:
        """Reset failure count on success"""
        ...

    async def delete(self, task_id: str) -> None:
        """Delete a task"""
        ...


class ScheduledTaskExecutionRepository(Protocol):
    """Repository interface for ScheduledTaskExecution"""

    async def save(self, execution: ScheduledTaskExecution) -> None:
        """Save or update an execution record"""
        ...

    async def find_by_id(self, execution_id: str) -> Optional[ScheduledTaskExecution]:
        """Find execution by ID"""
        ...

    async def find_by_task_id(self, task_id: str, limit: int = 20) -> List[ScheduledTaskExecution]:
        """Find executions for a task, ordered by scheduled_at desc"""
        ...

    async def find_by_user_id(self, user_id: str, limit: int = 50) -> List[ScheduledTaskExecution]:
        """Find executions for a user"""
        ...
