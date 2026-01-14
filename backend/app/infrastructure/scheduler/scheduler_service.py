import asyncio
import logging
from datetime import datetime, UTC
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from croniter import croniter
import pytz

from app.domain.models.scheduled_task import ScheduledTask, ScheduledTaskStatus
from app.domain.models.scheduled_task_execution import ScheduledTaskExecution, ExecutionStatus
from app.domain.repositories.scheduled_task_repository import (
    ScheduledTaskRepository,
    ScheduledTaskExecutionRepository
)

logger = logging.getLogger(__name__)

SCHEDULER_CHECK_INTERVAL = 60  # Check for due tasks every 60 seconds


class SchedulerService:
    """Service for managing scheduled task execution"""

    def __init__(
        self,
        task_repository: ScheduledTaskRepository,
        execution_repository: ScheduledTaskExecutionRepository,
    ):
        self._task_repository = task_repository
        self._execution_repository = execution_repository
        self._scheduler = AsyncIOScheduler()
        self._running = False
        self._agent_service = None  # Will be set via setter to avoid circular dependency
        self._email_service = None  # Will be set via setter

    def set_agent_service(self, agent_service) -> None:
        """Set agent service (to avoid circular dependency)"""
        self._agent_service = agent_service

    def set_email_service(self, email_service) -> None:
        """Set email service for notifications"""
        self._email_service = email_service

    async def start(self) -> None:
        """Start the scheduler service"""
        if self._running:
            return

        logger.info("Starting scheduler service")
        self._running = True

        # Add job to check for due tasks
        self._scheduler.add_job(
            self._check_due_tasks,
            'interval',
            seconds=SCHEDULER_CHECK_INTERVAL,
            id='check_due_tasks',
            replace_existing=True
        )

        self._scheduler.start()
        logger.info("Scheduler service started")

    async def stop(self) -> None:
        """Stop the scheduler service"""
        if not self._running:
            return

        logger.info("Stopping scheduler service")
        self._scheduler.shutdown(wait=True)
        self._running = False
        logger.info("Scheduler service stopped")

    def calculate_next_run(self, cron_expression: str, timezone: str = "UTC") -> datetime:
        """Calculate next run time from cron expression"""
        tz = pytz.timezone(timezone)
        base_time = datetime.now(tz)
        cron = croniter(cron_expression, base_time)
        return cron.get_next(datetime).astimezone(pytz.UTC)

    async def schedule_task(self, task: ScheduledTask) -> None:
        """Schedule a task for execution"""
        next_run = self.calculate_next_run(task.cron_expression, task.timezone)
        task.next_run_at = next_run
        await self._task_repository.update_next_run(task.id, next_run)
        logger.info(f"Scheduled task {task.id} for {next_run}")

    async def _check_due_tasks(self) -> None:
        """Check and execute due tasks"""
        try:
            now = datetime.now(UTC)
            due_tasks = await self._task_repository.find_due_tasks(now)

            for task in due_tasks:
                if task.status == ScheduledTaskStatus.ACTIVE:
                    asyncio.create_task(self._execute_task(task))

        except Exception as e:
            logger.exception(f"Error checking due tasks: {e}")

    async def _execute_task(self, task: ScheduledTask) -> None:
        """Execute a scheduled task"""
        execution = ScheduledTaskExecution(
            task_id=task.id,
            user_id=task.user_id,
            scheduled_at=task.next_run_at or datetime.now(UTC),
        )
        await self._execution_repository.save(execution)

        try:
            execution.start()
            await self._execution_repository.save(execution)

            if not self._agent_service:
                raise ValueError("AgentService not set")

            # Create a new session for this task
            session = await self._agent_service.create_session(task.user_id)
            execution.session_id = session.id

            # Execute the chat with the configured prompt
            # Note: We consume the generator to wait for completion
            async for event in self._agent_service.chat(
                session_id=session.id,
                user_id=task.user_id,
                message=task.config.prompt,
                attachments=[]  # TODO: Handle attachments if needed
            ):
                # Events are processed but we just need to wait for completion
                pass

            # Mark as completed
            execution.complete(summary=f"Task executed successfully in session {session.id}")
            await self._task_repository.reset_failure_count(task.id)

        except Exception as e:
            logger.exception(f"Error executing task {task.id}: {e}")
            execution.fail(str(e))
            await self._task_repository.increment_failure_count(task.id)

        finally:
            await self._execution_repository.save(execution)
            await self._task_repository.increment_run_count(task.id)
            await self._task_repository.update_last_run(
                task.id,
                datetime.now(UTC),
                execution.session_id or ""
            )

            # Schedule next run
            await self.schedule_task(task)

            # Send email notification if configured
            if task.config.notification_type == "email" and task.config.notification_email:
                await self._send_notification(task, execution)

    async def _send_notification(
        self,
        task: ScheduledTask,
        execution: ScheduledTaskExecution
    ) -> None:
        """Send email notification after task execution"""
        if not self._email_service:
            logger.warning("EmailService not set, skipping notification")
            return

        try:
            await self._email_service.send_task_notification(
                to_email=task.config.notification_email,
                task_name=task.name,
                result_summary=execution.result_summary or "任务执行完成",
                session_id=execution.session_id or "",
                execution_time=execution.completed_at or execution.started_at
            )
            execution.notification_sent = True
            await self._execution_repository.save(execution)
            logger.info(f"Notification sent for task {task.id} to {task.config.notification_email}")
        except Exception as e:
            logger.error(f"Failed to send notification for task {task.id}: {e}")
            execution.notification_error = str(e)
            await self._execution_repository.save(execution)
