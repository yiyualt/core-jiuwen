# coding: utf-8
"""TaskExecutor — wraps agent.run() with event emission."""

from typing import Any

from jiuwen.harness.task_loop.events import TaskEvent
from jiuwen.harness.task_loop.handler import EventHandler, LoggingHandler


class TaskExecutor:
    """Wraps an agent with event emission around its run() method.

    Usage::

        executor = TaskExecutor(agent, handlers=[LoggingHandler()])
        result = await executor.execute("Fix the bug in main.py")
    """

    def __init__(self, agent: Any, handlers: list[EventHandler] | None = None):
        self._agent = agent
        self._handlers = handlers or [LoggingHandler()]

    async def execute(self, task: str, session: Any = None) -> dict[str, Any]:
        """Execute a task and emit events.

        Args:
            task: The task description string.
            session: Optional session for multi-turn context.

        Returns:
            The agent's result dict.
        """
        await self._emit("task_start", {"task": task[:200]})

        try:
            result = await self._agent.run({"query": task}, session=session)
            await self._emit("task_complete", {"result": str(result.get("result", ""))[:500]})
            return result
        except Exception as e:
            await self._emit("error", {"error": str(e)})
            raise

    async def _emit(self, event_type: str, data: dict[str, Any]) -> None:
        event = TaskEvent(type=event_type, data=data)
        for handler in self._handlers:
            await handler.on_event(event)
