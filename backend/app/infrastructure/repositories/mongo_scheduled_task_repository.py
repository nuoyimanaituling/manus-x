from typing import Optional, List
from datetime import datetime, UTC
from app.domain.models.scheduled_task import ScheduledTask, ScheduledTaskStatus
from app.domain.models.scheduled_task_execution import ScheduledTaskExecution
from app.domain.repositories.scheduled_task_repository import (
    ScheduledTaskRepository,
    ScheduledTaskExecutionRepository
)
from app.infrastructure.models.documents import (
    ScheduledTaskDocument,
    ScheduledTaskExecutionDocument
)
import logging

logger = logging.getLogger(__name__)


class MongoScheduledTaskRepository(ScheduledTaskRepository):
    """MongoDB implementation of ScheduledTaskRepository"""

    async def save(self, task: ScheduledTask) -> None:
        """Save or update a scheduled task"""
        mongo_task = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task.id
        )

        if not mongo_task:
            mongo_task = ScheduledTaskDocument.from_domain(task)
            await mongo_task.save()
            return

        # Update fields from task domain model
        mongo_task.update_from_domain(task)
        await mongo_task.save()

    async def find_by_id(self, task_id: str) -> Optional[ScheduledTask]:
        """Find a task by ID"""
        mongo_task = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        )
        return mongo_task.to_domain() if mongo_task else None

    async def find_by_user_id(self, user_id: str) -> List[ScheduledTask]:
        """Find all tasks for a user"""
        mongo_tasks = await ScheduledTaskDocument.find(
            ScheduledTaskDocument.user_id == user_id
        ).sort("-created_at").to_list()
        return [mongo_task.to_domain() for mongo_task in mongo_tasks]

    async def find_by_id_and_user_id(self, task_id: str, user_id: str) -> Optional[ScheduledTask]:
        """Find a task by ID and user ID (for authorization)"""
        mongo_task = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id,
            ScheduledTaskDocument.user_id == user_id
        )
        return mongo_task.to_domain() if mongo_task else None

    async def find_active_tasks(self) -> List[ScheduledTask]:
        """Find all active tasks"""
        mongo_tasks = await ScheduledTaskDocument.find(
            ScheduledTaskDocument.status == ScheduledTaskStatus.ACTIVE
        ).to_list()
        return [mongo_task.to_domain() for mongo_task in mongo_tasks]

    async def find_due_tasks(self, before: datetime) -> List[ScheduledTask]:
        """Find tasks due to run before the given time"""
        mongo_tasks = await ScheduledTaskDocument.find(
            ScheduledTaskDocument.status == ScheduledTaskStatus.ACTIVE,
            ScheduledTaskDocument.next_run_at <= before
        ).to_list()
        return [mongo_task.to_domain() for mongo_task in mongo_tasks]

    async def update_next_run(self, task_id: str, next_run_at: datetime) -> None:
        """Update the next run time"""
        result = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        ).update(
            {"$set": {"next_run_at": next_run_at, "updated_at": datetime.now(UTC)}}
        )
        if not result:
            raise ValueError(f"Task {task_id} not found")

    async def update_last_run(self, task_id: str, last_run_at: datetime, session_id: str) -> None:
        """Update last run info"""
        result = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        ).update(
            {"$set": {"last_run_at": last_run_at, "last_session_id": session_id, "updated_at": datetime.now(UTC)}}
        )
        if not result:
            raise ValueError(f"Task {task_id} not found")

    async def update_status(self, task_id: str, status: ScheduledTaskStatus) -> None:
        """Update task status"""
        result = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        ).update(
            {"$set": {"status": status, "updated_at": datetime.now(UTC)}}
        )
        if not result:
            raise ValueError(f"Task {task_id} not found")

    async def increment_run_count(self, task_id: str) -> None:
        """Increment run count"""
        result = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        ).update(
            {"$inc": {"run_count": 1}, "$set": {"updated_at": datetime.now(UTC)}}
        )
        if not result:
            raise ValueError(f"Task {task_id} not found")

    async def increment_failure_count(self, task_id: str) -> None:
        """Increment failure count"""
        result = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        ).update(
            {"$inc": {"failure_count": 1}, "$set": {"updated_at": datetime.now(UTC)}}
        )
        if not result:
            raise ValueError(f"Task {task_id} not found")

    async def reset_failure_count(self, task_id: str) -> None:
        """Reset failure count on success"""
        result = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        ).update(
            {"$set": {"failure_count": 0, "updated_at": datetime.now(UTC)}}
        )
        if not result:
            raise ValueError(f"Task {task_id} not found")

    async def delete(self, task_id: str) -> None:
        """Delete a task"""
        mongo_task = await ScheduledTaskDocument.find_one(
            ScheduledTaskDocument.task_id == task_id
        )
        if mongo_task:
            await mongo_task.delete()


class MongoScheduledTaskExecutionRepository(ScheduledTaskExecutionRepository):
    """MongoDB implementation of ScheduledTaskExecutionRepository"""

    async def save(self, execution: ScheduledTaskExecution) -> None:
        """Save or update an execution record"""
        mongo_execution = await ScheduledTaskExecutionDocument.find_one(
            ScheduledTaskExecutionDocument.execution_id == execution.id
        )

        if not mongo_execution:
            mongo_execution = ScheduledTaskExecutionDocument.from_domain(execution)
            await mongo_execution.save()
            return

        mongo_execution.update_from_domain(execution)
        await mongo_execution.save()

    async def find_by_id(self, execution_id: str) -> Optional[ScheduledTaskExecution]:
        """Find execution by ID"""
        mongo_execution = await ScheduledTaskExecutionDocument.find_one(
            ScheduledTaskExecutionDocument.execution_id == execution_id
        )
        return mongo_execution.to_domain() if mongo_execution else None

    async def find_by_task_id(self, task_id: str, limit: int = 20) -> List[ScheduledTaskExecution]:
        """Find executions for a task, ordered by scheduled_at desc"""
        mongo_executions = await ScheduledTaskExecutionDocument.find(
            ScheduledTaskExecutionDocument.task_id == task_id
        ).sort("-scheduled_at").limit(limit).to_list()
        return [mongo_exec.to_domain() for mongo_exec in mongo_executions]

    async def find_by_user_id(self, user_id: str, limit: int = 50) -> List[ScheduledTaskExecution]:
        """Find executions for a user"""
        mongo_executions = await ScheduledTaskExecutionDocument.find(
            ScheduledTaskExecutionDocument.user_id == user_id
        ).sort("-scheduled_at").limit(limit).to_list()
        return [mongo_exec.to_domain() for mongo_exec in mongo_executions]
