from typing import List, Optional
import logging
from datetime import datetime, UTC

from app.domain.models.scheduled_task import ScheduledTask, ScheduledTaskStatus, ScheduledTaskConfig
from app.domain.models.scheduled_task_execution import ScheduledTaskExecution
from app.domain.repositories.scheduled_task_repository import (
    ScheduledTaskRepository,
    ScheduledTaskExecutionRepository
)
from app.infrastructure.scheduler.scheduler_service import SchedulerService

logger = logging.getLogger(__name__)


class ScheduledTaskService:
    """Application service for scheduled tasks"""

    def __init__(
        self,
        task_repository: ScheduledTaskRepository,
        execution_repository: ScheduledTaskExecutionRepository,
        scheduler_service: SchedulerService,
    ):
        self._task_repository = task_repository
        self._execution_repository = execution_repository
        self._scheduler_service = scheduler_service

    async def create_task(
        self,
        user_id: str,
        name: str,
        cron_expression: str,
        prompt: str,
        timezone: str = "UTC",
        description: Optional[str] = None,
        **config_kwargs
    ) -> ScheduledTask:
        """Create a new scheduled task"""
        config = ScheduledTaskConfig(prompt=prompt, **config_kwargs)

        task = ScheduledTask(
            user_id=user_id,
            name=name,
            description=description,
            cron_expression=cron_expression,
            timezone=timezone,
            config=config,
        )

        # Calculate and set next run time
        task.next_run_at = self._scheduler_service.calculate_next_run(
            cron_expression, timezone
        )

        await self._task_repository.save(task)
        logger.info(f"Created scheduled task {task.id} for user {user_id}")

        return task

    async def update_task(
        self,
        task_id: str,
        user_id: str,
        **updates
    ) -> Optional[ScheduledTask]:
        """Update a scheduled task"""
        task = await self._task_repository.find_by_id_and_user_id(task_id, user_id)
        if not task:
            return None

        # Update allowed fields
        for key, value in updates.items():
            if key == 'config' and isinstance(value, dict):
                # Update config fields
                for config_key, config_value in value.items():
                    setattr(task.config, config_key, config_value)
            elif hasattr(task, key) and key not in ('id', 'user_id', 'created_at'):
                setattr(task, key, value)

        task.updated_at = datetime.now(UTC)

        # Recalculate next run if cron changed
        if 'cron_expression' in updates or 'timezone' in updates:
            task.next_run_at = self._scheduler_service.calculate_next_run(
                task.cron_expression, task.timezone
            )

        await self._task_repository.save(task)
        return task

    async def get_task(self, task_id: str, user_id: str) -> Optional[ScheduledTask]:
        """Get a task by ID"""
        return await self._task_repository.find_by_id_and_user_id(task_id, user_id)

    async def get_user_tasks(self, user_id: str) -> List[ScheduledTask]:
        """Get all tasks for a user"""
        return await self._task_repository.find_by_user_id(user_id)

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task"""
        task = await self._task_repository.find_by_id_and_user_id(task_id, user_id)
        if not task:
            return False

        await self._task_repository.delete(task_id)
        return True

    async def pause_task(self, task_id: str, user_id: str) -> Optional[ScheduledTask]:
        """Pause a task"""
        task = await self._task_repository.find_by_id_and_user_id(task_id, user_id)
        if not task:
            return None

        task.pause()
        await self._task_repository.save(task)
        return task

    async def resume_task(self, task_id: str, user_id: str) -> Optional[ScheduledTask]:
        """Resume a paused task"""
        task = await self._task_repository.find_by_id_and_user_id(task_id, user_id)
        if not task:
            return None

        task.resume()
        # Recalculate next run
        task.next_run_at = self._scheduler_service.calculate_next_run(
            task.cron_expression, task.timezone
        )
        await self._task_repository.save(task)
        return task

    async def run_task_now(self, task_id: str, user_id: str) -> Optional[ScheduledTaskExecution]:
        """Manually trigger a task execution"""
        task = await self._task_repository.find_by_id_and_user_id(task_id, user_id)
        if not task:
            return None

        # Execute task immediately
        await self._scheduler_service._execute_task(task)

        # Return the latest execution
        executions = await self._execution_repository.find_by_task_id(task_id, limit=1)
        return executions[0] if executions else None

    async def get_task_executions(
        self, task_id: str, user_id: str, limit: int = 20
    ) -> List[ScheduledTaskExecution]:
        """Get execution history for a task"""
        task = await self._task_repository.find_by_id_and_user_id(task_id, user_id)
        if not task:
            return []

        return await self._execution_repository.find_by_task_id(task_id, limit)

    async def get_user_executions(self, user_id: str, limit: int = 50) -> List[ScheduledTaskExecution]:
        """Get all executions for a user"""
        return await self._execution_repository.find_by_user_id(user_id, limit)
