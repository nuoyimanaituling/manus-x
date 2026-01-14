"""Scheduled task tool for creating scheduled tasks via Agent conversation"""

from typing import Optional
import logging

from app.domain.services.tools.base import tool, BaseTool
from app.domain.models.tool_result import ToolResult

logger = logging.getLogger(__name__)


class ScheduledTaskTool(BaseTool):
    """Tool for creating and managing scheduled tasks through Agent conversation.

    This tool allows the Agent to create scheduled tasks when users express
    intentions like "every day at 8 AM help me generate a news report".
    The Agent is responsible for parsing natural language time expressions
    into cron expressions.
    """

    name: str = "scheduled_task"

    def __init__(self, scheduled_task_service, user_id: str):
        """Initialize the scheduled task tool.

        Args:
            scheduled_task_service: The ScheduledTaskService instance
            user_id: The ID of the current user
        """
        super().__init__()
        self._scheduled_task_service = scheduled_task_service
        self._user_id = user_id

    @tool(
        name="scheduled_task_create",
        description="""Create a scheduled task that will automatically execute at specified times.
Use this tool when user wants to set up recurring tasks, automated reports, or scheduled reminders.

The task will:
1. Run the specified prompt at the scheduled time using AI Agent
2. Optionally send email notification with results

Common time patterns to cron conversion:
- "每天8点" / "daily at 8 AM" → "0 8 * * *"
- "每天早上9点" / "every morning at 9" → "0 9 * * *"
- "工作日9点" / "weekdays at 9 AM" → "0 9 * * 1-5"
- "每周一10点" / "every Monday at 10 AM" → "0 10 * * 1"
- "每小时" / "every hour" → "0 * * * *"
- "每2小时" / "every 2 hours" → "0 */2 * * *"
- "每月1号9点" / "first day of month at 9 AM" → "0 9 1 * *"

IMPORTANT: Before creating the task, you should:
1. Confirm the task details with the user
2. Ask for email address if user wants notification""",
        parameters={
            "name": {
                "type": "string",
                "description": "A short, descriptive name for the task (e.g., '每日热点新闻报告', 'Daily News Report')"
            },
            "cron_expression": {
                "type": "string",
                "description": "Cron expression for scheduling (minute hour day month weekday). Examples: '0 8 * * *' for daily 8 AM, '0 9 * * 1-5' for weekdays 9 AM"
            },
            "prompt": {
                "type": "string",
                "description": "The task content/instruction that the AI Agent will execute at scheduled time. Should be detailed enough for the Agent to understand what to do."
            },
            "timezone": {
                "type": "string",
                "description": "Timezone for the schedule (e.g., 'Asia/Shanghai', 'UTC', 'America/New_York'). Default: 'Asia/Shanghai'"
            },
            "description": {
                "type": "string",
                "description": "Optional detailed description of the task purpose"
            },
            "notification_email": {
                "type": "string",
                "description": "Email address to send notification after task execution. If provided, email notification will be enabled."
            }
        },
        required=["name", "cron_expression", "prompt"]
    )
    async def scheduled_task_create(
        self,
        name: str,
        cron_expression: str,
        prompt: str,
        timezone: str = "Asia/Shanghai",
        description: Optional[str] = None,
        notification_email: Optional[str] = None
    ) -> ToolResult:
        """Create a new scheduled task.

        Args:
            name: Task name
            cron_expression: Cron expression for scheduling
            prompt: Task content for AI to execute
            timezone: Timezone for the schedule
            description: Optional task description
            notification_email: Optional email for notification

        Returns:
            ToolResult with task creation status
        """
        try:
            # Determine notification type based on email
            notification_type = "email" if notification_email else "none"

            task = await self._scheduled_task_service.create_task(
                user_id=self._user_id,
                name=name,
                cron_expression=cron_expression,
                prompt=prompt,
                timezone=timezone,
                description=description,
                notification_type=notification_type,
                notification_email=notification_email
            )

            # Format next run time for display
            next_run_str = task.next_run_at.strftime("%Y-%m-%d %H:%M:%S %Z") if task.next_run_at else "N/A"

            result_message = f"""定时任务创建成功！

任务详情:
- 任务名称: {task.name}
- 执行计划: {task.cron_expression} ({timezone})
- 下次执行: {next_run_str}
- 任务ID: {task.id}"""

            if notification_email:
                result_message += f"\n- 通知邮箱: {notification_email}"

            logger.info(f"Created scheduled task {task.id} for user {self._user_id}")

            return ToolResult(
                success=True,
                message=result_message,
                data={
                    "task_id": task.id,
                    "name": task.name,
                    "cron_expression": task.cron_expression,
                    "timezone": task.timezone,
                    "next_run_at": task.next_run_at.isoformat() if task.next_run_at else None,
                    "notification_email": notification_email
                }
            )

        except Exception as e:
            logger.error(f"Failed to create scheduled task: {e}")
            return ToolResult(
                success=False,
                message=f"创建定时任务失败: {str(e)}"
            )
