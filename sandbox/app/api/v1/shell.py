from fastapi import APIRouter
from app.schemas.shell import (
    ShellExecRequest, ShellViewRequest, ShellWaitRequest,
    ShellWriteToProcessRequest, ShellKillProcessRequest,
)
from app.schemas.response import Response
from app.services.shell import shell_service
from app.core.exceptions import BadRequestException

router = APIRouter()

@router.post("/exec", response_model=Response)
async def exec_command(request: ShellExecRequest):
    """
    Execute command in the specified shell session
    """
    # If no session ID is provided, automatically create one
    if not request.id or request.id == "":
        request.id = shell_service.create_session_id()
        
    result = await shell_service.exec_command(
        session_id=request.id,
        exec_dir=request.exec_dir,
        command=request.command
    )
    
    # Construct response
    return Response(
        success=True,
        message="Command executed",
        data=result.model_dump()
    )

@router.post("/view", response_model=Response)
async def view_shell(request: ShellViewRequest):
    """
    View output of the specified shell session
    """
    if not request.id or request.id == "":
        raise BadRequestException("Session ID not provided")
        
    result = await shell_service.view_shell(session_id=request.id, console=request.console)
    
    # Construct response
    return Response(
        success=True,
        message="Session content retrieved successfully",
        data=result.model_dump()
    )

@router.post("/wait", response_model=Response)
async def wait_for_process(request: ShellWaitRequest):
    """
    Wait for the process in the specified shell session to return
    """
    result = await shell_service.wait_for_process(
        session_id=request.id,
        seconds=request.seconds
    )
    
    # Construct response
    return Response(
        success=True,
        message=f"Process completed, return code: {result.returncode}",
        data=result.model_dump()
    )

@router.post("/write", response_model=Response)
async def write_to_process(request: ShellWriteToProcessRequest):
    """
    Write input to the process in the specified shell session
    """
    if not request.id or request.id == "":
        raise BadRequestException("Session ID not provided")
        
    result = await shell_service.write_to_process(
        session_id=request.id,
        input_text=request.input,
        press_enter=request.press_enter
    )
    
    # Construct response
    return Response(
        success=True,
        message="Input written",
        data=result.model_dump()
    )

@router.post("/kill", response_model=Response)
async def kill_process(request: ShellKillProcessRequest):
    """
    Terminate the process in the specified shell session
    """
    result = await shell_service.kill_process(session_id=request.id)
    
    # Construct response
    message = "Process terminated" if result.status == "terminated" else "Process ended"
    return Response(
        success=True,
        message=message,
        data=result.model_dump()
    )