from typing import Optional, Dict, Any
from app.domain.external.sandbox import Sandbox
from app.domain.services.tools.base import tool, BaseTool
from app.domain.models.tool_result import ToolResult

class FileTool(BaseTool):
    """File tool class, providing file operation functions"""

    name: str = "file"
    
    def __init__(self, sandbox: Sandbox):
        """Initialize file tool class
        
        Args:
            sandbox: Sandbox service
        """
        super().__init__()
        self.sandbox = sandbox
        
    @tool(
        name="file_read",
        description="Read file content. Use for checking file contents, analyzing logs, or reading configuration files.",
        parameters={
            "file": {
                "type": "string",
                "description": "Absolute path of the file to read"
            },
            "start_line": {
                "type": "integer",
                "description": "(Optional) Starting line to read from, 0-based"
            },
            "end_line": {
                "type": "integer",
                "description": "(Optional) Ending line number (exclusive)"
            },
            "sudo": {
                "type": "boolean",
                "description": "(Optional) Whether to use sudo privileges"
            }
        },
        required=["file"]
    )
    async def file_read(
        self,
        file: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        sudo: Optional[bool] = False
    ) -> ToolResult:
        """Read file content
        
        Args:
            file: Absolute path of the file to read
            start_line: (Optional) Starting line, 0-based
            end_line: (Optional) Ending line (exclusive)
            sudo: (Optional) Whether to use sudo privileges
            
        Returns:
            File content
        """
        # Directly call sandbox's file_read method
        return await self.sandbox.file_read(
            file=file,
            start_line=start_line,
            end_line=end_line,
            sudo=sudo
        )
    
    @tool(
        name="file_write",
        description="Overwrite or append content to a file. Use for creating new files, appending content, or modifying existing files.",
        parameters={
            "file": {
                "type": "string",
                "description": "Absolute path of the file to write to"
            },
            "content": {
                "type": "string",
                "description": "Text content to write"
            },
            "append": {
                "type": "boolean",
                "description": "(Optional) Whether to use append mode"
            },
            "leading_newline": {
                "type": "boolean",
                "description": "(Optional) Whether to add a leading newline"
            },
            "trailing_newline": {
                "type": "boolean",
                "description": "(Optional) Whether to add a trailing newline"
            },
            "sudo": {
                "type": "boolean",
                "description": "(Optional) Whether to use sudo privileges"
            }
        },
        required=["file", "content"]
    )
    async def file_write(
        self,
        file: str,
        content: str,
        append: Optional[bool] = False,
        leading_newline: Optional[bool] = False,
        trailing_newline: Optional[bool] = False,
        sudo: Optional[bool] = False
    ) -> ToolResult:
        """Write content to file
        
        Args:
            file: Absolute path of the file to write to
            content: Text content to write
            append: (Optional) Whether to use append mode
            leading_newline: (Optional) Whether to add a leading newline
            trailing_newline: (Optional) Whether to add a trailing newline
            sudo: (Optional) Whether to use sudo privileges
            
        Returns:
            Write result
        """
        # Prepare content
        final_content = content
        if leading_newline:
            final_content = "\n" + final_content
        if trailing_newline:
            final_content = final_content + "\n"
            
        # Directly call sandbox's file_write method, pass all parameters
        return await self.sandbox.file_write(
            file=file, 
            content=final_content,
            append=append,
            leading_newline=False,  # Already handled in final_content
            trailing_newline=False,  # Already handled in final_content
            sudo=sudo
        )
    
    @tool(
        name="file_str_replace",
        description="Replace specified string in a file. Use for updating specific content in files or fixing errors in code.",
        parameters={
            "file": {
                "type": "string",
                "description": "Absolute path of the file to perform replacement on"
            },
            "old_str": {
                "type": "string",
                "description": "Original string to be replaced"
            },
            "new_str": {
                "type": "string",
                "description": "New string to replace with"
            },
            "sudo": {
                "type": "boolean",
                "description": "(Optional) Whether to use sudo privileges"
            }
        },
        required=["file", "old_str", "new_str"]
    )
    async def file_str_replace(
        self,
        file: str,
        old_str: str,
        new_str: str,
        sudo: Optional[bool] = False
    ) -> ToolResult:
        """Replace specified string in file
        
        Args:
            file: Absolute path of the file to perform replacement on
            old_str: Original string to be replaced
            new_str: New string to replace with
            sudo: (Optional) Whether to use sudo privileges
            
        Returns:
            Replacement result
        """
        # Directly call sandbox's file_replace method
        return await self.sandbox.file_replace(
            file=file,
            old_str=old_str,
            new_str=new_str,
            sudo=sudo
        )
    
    @tool(
        name="file_find_in_content",
        description="Search for matching text within file content. Use for finding specific content or patterns in files.",
        parameters={
            "file": {
                "type": "string",
                "description": "Absolute path of the file to search within"
            },
            "regex": {
                "type": "string",
                "description": "Regular expression pattern to match"
            },
            "sudo": {
                "type": "boolean",
                "description": "(Optional) Whether to use sudo privileges"
            }
        },
        required=["file", "regex"]
    )
    async def file_find_in_content(
        self,
        file: str,
        regex: str,
        sudo: Optional[bool] = False
    ) -> ToolResult:
        """Search for matching text in file content
        
        Args:
            file: Absolute path of the file to search
            regex: Regular expression pattern for matching
            sudo: (Optional) Whether to use sudo privileges
            
        Returns:
            Search results
        """
        # Directly call sandbox's file_search method
        return await self.sandbox.file_search(
            file=file,
            regex=regex,
            sudo=sudo
        )
    
    @tool(
        name="file_find_by_name",
        description="Find files by name pattern in specified directory. Use for locating files with specific naming patterns.",
        parameters={
            "path": {
                "type": "string",
                "description": "Absolute path of directory to search"
            },
            "glob": {
                "type": "string",
                "description": "Filename pattern using glob syntax wildcards"
            }
        },
        required=["path", "glob"]
    )
    async def file_find_by_name(
        self,
        path: str,
        glob: str
    ) -> ToolResult:
        """Find files by name pattern in specified directory
        
        Args:
            path: Absolute path of directory to search
            glob: Filename pattern using glob syntax wildcards
            
        Returns:
            Search results
        """
        # Directly call sandbox's file_find method
        return await self.sandbox.file_find(
            path=path,
            glob_pattern=glob
        ) 