from typing import Optional
from app.domain.external.sandbox import Sandbox
from app.domain.services.tools.base import tool, BaseTool
from app.domain.models.tool_result import ToolResult

class ShellTool(BaseTool):
    """Shell tool class, providing Shell interaction related functions"""

    name: str = "shell"
    
    def __init__(self, sandbox: Sandbox):
        """Initialize Shell tool class
        
        Args:
            sandbox: Sandbox service
        """
        super().__init__()
        self.sandbox = sandbox
        
    @tool(
        name="shell_exec",
        description="Execute commands in a specified shell session. Use for running code, installing packages, or managing files.",
        parameters={
            "id": {
                "type": "string",
                "description": "Unique identifier of the target shell session"
            },
            "exec_dir": {
                "type": "string",
                "description": "Working directory for command execution (must use absolute path)"
            },
            "command": {
                "type": "string",
                "description": "Shell command to execute"
            }
        },
        required=["id", "exec_dir", "command"]
    )
    async def shell_exec(
        self,
        id: str,
        exec_dir: str,
        command: str
    ) -> ToolResult:
        """Execute Shell command
        
        Args:
            id: Unique identifier of the target Shell session
            exec_dir: Working directory for command execution (must use absolute path)
            command: Shell command to execute
            
        Returns:
            Command execution result
        """
        return await self.sandbox.exec_command(id, exec_dir, command)
    
    @tool(
        name="shell_view",
        description="View the content of a specified shell session. Use for checking command execution results or monitoring output.",
        parameters={
            "id": {
                "type": "string",
                "description": "Unique identifier of the target shell session"
            }
        },
        required=["id"]
    )
    async def shell_view(self, id: str) -> ToolResult:
        """View Shell session content
        
        Args:
            id: Unique identifier of the target Shell session
            
        Returns:
            Shell session content
        """
        return await self.sandbox.view_shell(id)
    
    @tool(
        name="shell_wait",
        description="Wait for the running process in a specified shell session to return. Use after running commands that require longer runtime.",
        parameters={
            "id": {
                "type": "string",
                "description": "Unique identifier of the target shell session"
            },
            "seconds": {
                "type": "integer",
                "description": "Wait duration in seconds"
            }
        },
        required=["id"]
    )
    async def shell_wait(
        self,
        id: str,
        seconds: Optional[int] = None
    ) -> ToolResult:
        """Wait for the running process in Shell session to return
        
        Args:
            id: Unique identifier of the target Shell session
            seconds: Wait time (seconds)
            
        Returns:
            Wait result
        """
        return await self.sandbox.wait_for_process(id, seconds)
    
    @tool(
        name="shell_write_to_process",
        description="Write input to a running process in a specified shell session. Use for responding to interactive command prompts.",
        parameters={
            "id": {
                "type": "string",
                "description": "Unique identifier of the target shell session"
            },
            "input": {
                "type": "string",
                "description": "Input content to write to the process"
            },
            "press_enter": {
                "type": "boolean",
                "description": "Whether to press Enter key after input"
            }
        },
        required=["id", "input", "press_enter"]
    )
    async def shell_write_to_process(
        self,
        id: str,
        input: str,
        press_enter: bool
    ) -> ToolResult:
        """Write input to the running process in Shell session
        
        Args:
            id: Unique identifier of the target Shell session
            input: Input content to write to the process
            press_enter: Whether to press Enter key after input
            
        Returns:
            Write result
        """
        return await self.sandbox.write_to_process(id, input, press_enter)
    
    @tool(
        name="shell_kill_process",
        description="Terminate a running process in a specified shell session. Use for stopping long-running processes or handling frozen commands.",
        parameters={
            "id": {
                "type": "string",
                "description": "Unique identifier of the target shell session"
            }
        },
        required=["id"]
    )
    async def shell_kill_process(self, id: str) -> ToolResult:
        """Terminate the running process in Shell session
        
        Args:
            id: Unique identifier of the target Shell session
            
        Returns:
            Termination result
        """
        return await self.sandbox.kill_process(id)
