from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.domain.models.user import User
from app.interfaces.dependencies import get_current_user, get_scheduled_task_service
from app.application.services.scheduled_task_service import ScheduledTaskService

router = APIRouter(prefix="/scheduled-tasks", tags=["scheduled-tasks"])


# Request/Response Schemas
class CreateScheduledTaskRequest(BaseModel):
    name: str
    cron_expression: str
    prompt: str
    timezone: str = "UTC"
    description: Optional[str] = None
    save_result: bool = True
    notification_type: str = "none"
    notification_email: Optional[str] = None
    attachments: List[str] = []


class UpdateScheduledTaskRequest(BaseModel):
    name: Optional[str] = None
    cron_expression: Optional[str] = None
    prompt: Optional[str] = None
    timezone: Optional[str] = None
    description: Optional[str] = None


class ScheduledTaskResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    cron_expression: str
    timezone: str
    status: str
    prompt: str
    next_run_at: Optional[int]  # Unix timestamp
    last_run_at: Optional[int]
    run_count: int
    created_at: int


class ScheduledTaskExecutionResponse(BaseModel):
    id: str
    task_id: str
    session_id: Optional[str]
    status: str
    scheduled_at: int
    started_at: Optional[int]
    completed_at: Optional[int]
    result_summary: Optional[str]
    error_message: Optional[str]


# Routes
@router.post("", response_model=ScheduledTaskResponse)
async def create_task(
    request: CreateScheduledTaskRequest,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Create a new scheduled task"""
    task = await service.create_task(
        user_id=current_user.id,
        name=request.name,
        cron_expression=request.cron_expression,
        prompt=request.prompt,
        timezone=request.timezone,
        description=request.description,
        save_result=request.save_result,
        notification_type=request.notification_type,
        notification_email=request.notification_email,
        attachments=request.attachments,
    )
    return _task_to_response(task)


@router.get("", response_model=List[ScheduledTaskResponse])
async def list_tasks(
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """List all scheduled tasks for current user"""
    tasks = await service.get_user_tasks(current_user.id)
    return [_task_to_response(t) for t in tasks]


@router.get("/{task_id}", response_model=ScheduledTaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Get a specific scheduled task"""
    task = await service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Scheduled task not found")
    return _task_to_response(task)


@router.put("/{task_id}", response_model=ScheduledTaskResponse)
async def update_task(
    task_id: str,
    request: UpdateScheduledTaskRequest,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Update a scheduled task"""
    updates = request.model_dump(exclude_unset=True)
    if 'prompt' in updates:
        if 'config' not in updates:
            updates['config'] = {}
        updates['config']['prompt'] = updates.pop('prompt')

    task = await service.update_task(task_id, current_user.id, **updates)
    if not task:
        raise HTTPException(status_code=404, detail="Scheduled task not found")
    return _task_to_response(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Delete a scheduled task"""
    success = await service.delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Scheduled task not found")


@router.post("/{task_id}/pause", response_model=ScheduledTaskResponse)
async def pause_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Pause a scheduled task"""
    task = await service.pause_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Scheduled task not found")
    return _task_to_response(task)


@router.post("/{task_id}/resume", response_model=ScheduledTaskResponse)
async def resume_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Resume a paused scheduled task"""
    task = await service.resume_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Scheduled task not found")
    return _task_to_response(task)


@router.post("/{task_id}/run", response_model=ScheduledTaskExecutionResponse)
async def run_task_now(
    task_id: str,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Manually trigger a task execution"""
    execution = await service.run_task_now(task_id, current_user.id)
    if not execution:
        raise HTTPException(status_code=404, detail="Scheduled task not found")
    return _execution_to_response(execution)


@router.get("/{task_id}/executions", response_model=List[ScheduledTaskExecutionResponse])
async def get_task_executions(
    task_id: str,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    service: ScheduledTaskService = Depends(get_scheduled_task_service)
):
    """Get execution history for a task"""
    executions = await service.get_task_executions(task_id, current_user.id, limit)
    return [_execution_to_response(e) for e in executions]


# Helper functions
def _task_to_response(task) -> ScheduledTaskResponse:
    return ScheduledTaskResponse(
        id=task.id,
        name=task.name,
        description=task.description,
        cron_expression=task.cron_expression,
        timezone=task.timezone,
        status=task.status.value,
        prompt=task.config.prompt,
        next_run_at=int(task.next_run_at.timestamp()) if task.next_run_at else None,
        last_run_at=int(task.last_run_at.timestamp()) if task.last_run_at else None,
        run_count=task.run_count,
        created_at=int(task.created_at.timestamp()),
    )


def _execution_to_response(execution) -> ScheduledTaskExecutionResponse:
    return ScheduledTaskExecutionResponse(
        id=execution.id,
        task_id=execution.task_id,
        session_id=execution.session_id,
        status=execution.status.value,
        scheduled_at=int(execution.scheduled_at.timestamp()),
        started_at=int(execution.started_at.timestamp()) if execution.started_at else None,
        completed_at=int(execution.completed_at.timestamp()) if execution.completed_at else None,
        result_summary=execution.result_summary,
        error_message=execution.error_message,
    )
