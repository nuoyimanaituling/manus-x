"""
业务模型定义
"""
from app.models.shell import ShellExecResult, ShellViewResult, ShellWaitResult, ShellWriteResult, ShellKillResult
from app.models.supervisor import ProcessInfo, SupervisorActionResult, SupervisorTimeout
from app.models.file import FileReadResult, FileWriteResult, FileReplaceResult, FileSearchResult, FileFindResult

__all__ = [
    'ShellExecResult', 'ShellViewResult', 'ShellWaitResult', 'ShellWriteResult', 'ShellKillResult',
    'ProcessInfo', 'SupervisorActionResult', 'SupervisorTimeout',
    'FileReadResult', 'FileWriteResult', 'FileReplaceResult', 'FileSearchResult', 'FileFindResult'
]
