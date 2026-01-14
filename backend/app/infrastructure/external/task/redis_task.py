import asyncio
import uuid
import logging
from typing import Optional, Dict

from app.domain.external.task import Task, TaskRunner
from app.infrastructure.external.message_queue.redis_stream_queue import RedisStreamQueue, MessageQueue

logger = logging.getLogger(__name__)


class RedisStreamTask(Task):
    """Redis Stream-based task implementation following the Task protocol."""
    
    _task_registry: Dict[str, 'RedisStreamTask'] = {}
    
    def __init__(self, runner: TaskRunner):
        """Initialize Redis Stream task with a task runner.
        
        Args:
            runner: The TaskRunner instance that will execute this task
        """
        self._runner = runner
        self._id = str(uuid.uuid4())
        self._execution_task: Optional[asyncio.Task] = None
        
        # Create input/output streams based on task ID
        input_stream_name = f"task:input:{self._id}"
        output_stream_name = f"task:output:{self._id}"
        self._input_stream = RedisStreamQueue(input_stream_name)
        self._output_stream = RedisStreamQueue(output_stream_name)
        
        # Register task instance
        RedisStreamTask._task_registry[self._id] = self
        
    @property
    def id(self) -> str:
        """Task ID."""
        return self._id
    
    @property
    def done(self) -> bool:
        """Check if the task is done.

        Returns:
            bool: True if the task is done, False otherwise
        """
        if self._execution_task is None:
            return True
        return self._execution_task.done()
    
    async def run(self) -> None:
        """Run the task using the provided TaskRunner."""
        if self.done:
            self._execution_task = asyncio.create_task(self._execute_task())
            logger.info(f"Task {self._id} execution started")
    
    def cancel(self) -> bool:
        """Cancel the task.

        Returns:
            bool: True if the task is cancelled, False otherwise
        """
        if not self.done:
            self._execution_task.cancel()
            logger.info(f"Task {self._id} cancelled")
            self._cleanup_registry()
            return True
        
        self._cleanup_registry()
        return False
    
    @property
    def input_stream(self) -> MessageQueue:
        """Input stream."""
        return self._input_stream
    
    @property
    def output_stream(self) -> MessageQueue:
        """Output stream."""
        return self._output_stream
    
    def _on_task_done(self) -> None:
        """Called when the task is done."""
        self._task_done = True
        if self._runner:
            asyncio.create_task(self._runner.on_done(self))
        self._cleanup_registry()
    
    def _cleanup_registry(self) -> None:
        """Remove this task from the registry."""
        if self._id in RedisStreamTask._task_registry:
            del RedisStreamTask._task_registry[self._id]
            logger.info(f"Task {self._id} removed from registry")
    
    async def _execute_task(self):
        """Execute the task using the TaskRunner."""
        try:
            await self._runner.run(self)
        except asyncio.CancelledError:
            logger.info(f"Task {self._id} execution cancelled")
        except Exception as e:
            logger.error(f"Task {self._id} execution failed: {str(e)}")
        finally:
            self._on_task_done()
    
    @classmethod
    def get(cls, task_id: str) -> Optional['RedisStreamTask']:
        """Get a task by its ID.

        Returns:
            Optional[RedisStreamTask]: Task instance if found, None otherwise
        """
        return cls._task_registry.get(task_id)
    
    @classmethod
    def create(cls, runner: TaskRunner) -> "RedisStreamTask":
        """Create a new task instance with the specified TaskRunner.

        Args:
            runner: The TaskRunner that will execute this task

        Returns:
            RedisStreamTask: New task instance
        """
        return cls(runner)

    @classmethod
    async def destroy(cls) -> None:
        """Destroy all task instances."""
        for task_id in cls._task_registry:
            task = cls._task_registry[task_id]
            task.cancel()
            if task._runner:
                await task._runner.destroy()
        cls._task_registry.clear()
    
    def __repr__(self) -> str:
        """String representation of the task."""
        return f"RedisStreamTask(id={self._id}, done={self.done})"