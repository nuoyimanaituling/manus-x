from pydantic import BaseModel, Field, field_validator
from datetime import datetime, UTC
from typing import Optional, List
from enum import Enum
import uuid


class ScheduledTaskStatus(str, Enum):
    """Scheduled task status"""
    ACTIVE = "active"        # Task is active and will execute on schedule
    PAUSED = "paused"        # Task is paused
    DISABLED = "disabled"    # Task is disabled


class NotificationType(str, Enum):
    """Notification type after task execution"""
    NONE = "none"
    EMAIL = "email"


class ScheduledTaskConfig(BaseModel):
    """Configuration for scheduled task execution"""
    prompt: str                                    # The prompt/message to send to Agent
    save_result: bool = True                       # Save execution result/files
    notification_type: NotificationType = NotificationType.NONE
    notification_email: Optional[str] = None       # Email for notification
    attachments: List[str] = []                    # File IDs to attach


class ScheduledTask(BaseModel):
    """Scheduled task domain model"""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    user_id: str                                   # Owner of this task
    name: str                                      # Human-readable task name
    description: Optional[str] = None              # Optional description
    cron_expression: str                           # Cron expression for scheduling
    timezone: str = "UTC"                          # Timezone for cron interpretation
    config: ScheduledTaskConfig                    # Execution configuration
    status: ScheduledTaskStatus = ScheduledTaskStatus.ACTIVE

    # Execution tracking
    next_run_at: Optional[datetime] = None         # Next scheduled execution time
    last_run_at: Optional[datetime] = None         # Last execution time
    last_session_id: Optional[str] = None          # Session ID of last execution
    run_count: int = 0                             # Total execution count
    failure_count: int = 0                         # Consecutive failure count

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("cron_expression")
    @classmethod
    def validate_cron(cls, v: str) -> str:
        """Validate cron expression format"""
        parts = v.strip().split()
        if len(parts) not in (5, 6):  # Standard 5-field or with seconds
            raise ValueError("Invalid cron expression: must have 5 or 6 fields")
        return v.strip()

    def pause(self) -> None:
        """Pause the scheduled task"""
        self.status = ScheduledTaskStatus.PAUSED
        self.updated_at = datetime.now(UTC)

    def resume(self) -> None:
        """Resume the scheduled task"""
        self.status = ScheduledTaskStatus.ACTIVE
        self.updated_at = datetime.now(UTC)

    def disable(self) -> None:
        """Disable the scheduled task"""
        self.status = ScheduledTaskStatus.DISABLED
        self.updated_at = datetime.now(UTC)
