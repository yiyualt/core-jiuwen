# coding: utf-8
"""LoopCoordinator — async task queue manager."""

import asyncio
from typing import Any

from jiuwen.harness.task_loop.executor import TaskExecutor


class LoopCoordinator:
    """Manages an async queue of tasks for sequential execution.

    Usage::

        coordinator = LoopCoordinator(executor)
        await coordinator.submit("Fix bug #1")
        await coordinator.submit("Fix bug #2")
        await coordinator.submit(None)  # stop signal
        await coordinator.run()
    """

    def __init__(self, executor: TaskExecutor):
        self._executor = executor
        self._queue: asyncio.Queue[tuple[str, Any] | None] = asyncio.Queue()

    async def submit(self, task: str, session: Any = None) -> None:
        """Enqueue a task for execution.

        Args:
            task: Task description string. None = stop signal.
            session: Optional session.
        """
        await self._queue.put((task, session) if task is not None else None)

    async def run(self) -> None:
        """Process the queue until a stop signal is received."""
        while True:
            item = await self._queue.get()
            if item is None:
                break
            task, session = item
            await self._executor.execute(task, session)
