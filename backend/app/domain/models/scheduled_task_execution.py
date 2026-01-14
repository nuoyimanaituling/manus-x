from pydantic import BaseModel, Field
from datetime import datetime, UTC
from typing import Optional, List
from enum import Enum
import uuid


class ExecutionStatus(str, Enum):
    """Execution status"""
    PENDING = "pending"      # Waiting to start
    RUNNING = "running"      # Currently executing
    COMPLETED = "completed"  # Successfully completed
    FAILED = "failed"        # Execution failed
    CANCELLED = "cancelled"  # Manually cancelled


class ScheduledTaskExecution(BaseModel):
    """Record of a scheduled task execution"""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    task_id: str                                   # Reference to ScheduledTask
    user_id: str                                   # Task owner
    session_id: Optional[str] = None               # Created session ID

    status: ExecutionStatus = ExecutionStatus.PENDING
    scheduled_at: datetime                         # When it was scheduled to run
    started_at: Optional[datetime] = None          # Actual start time
    completed_at: Optional[datetime] = None        # Completion time

    # Results
    result_summary: Optional[str] = None           # Summary of execution result
    error_message: Optional[str] = None            # Error if failed
    output_files: List[str] = []                   # Generated file IDs

    # Notification
    notification_sent: bool = False
    notification_error: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def start(self) -> None:
        """Mark execution as started"""
        self.status = ExecutionStatus.RUNNING
        self.started_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def complete(self, summary: Optional[str] = None) -> None:
        """Mark execution as completed"""
        self.status = ExecutionStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self.result_summary = summary
        self.updated_at = datetime.now(UTC)

    def fail(self, error: str) -> None:
        """Mark execution as failed"""
        self.status = ExecutionStatus.FAILED
        self.completed_at = datetime.now(UTC)
        self.error_message = error
        self.updated_at = datetime.now(UTC)

    def cancel(self) -> None:
        """Mark execution as cancelled"""
        self.status = ExecutionStatus.CANCELLED
        self.completed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
