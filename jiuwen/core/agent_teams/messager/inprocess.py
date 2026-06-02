# coding: utf-8
"""InProcessMessager — async message passing between agents in the same process."""

import asyncio


class InProcessMessager:
    """Async message queue for agents running in the same process.

    Each agent has a named inbox. Messages are delivered via async queues.

    Usage::

        msgr = InProcessMessager()
        await msgr.send("agent_b", {"task": "search", "query": "AI"})
        msg = await msgr.receive("agent_b")
    """

    def __init__(self):
        self._queues: dict[str, asyncio.Queue] = {}

    async def send(self, target: str, message: dict) -> None:
        """Send a message to an agent's inbox.

        Args:
            target: Name of the receiving agent.
            message: Message dict to deliver.
        """
        queue = self._queues.setdefault(target, asyncio.Queue())
        await queue.put(message)

    async def receive(self, agent_name: str, timeout: float | None = None) -> dict:
        """Receive a message from an agent's inbox.

        Args:
            agent_name: Name of this agent.
            timeout: Optional timeout in seconds.

        Returns:
            The received message dict.

        Raises:
            asyncio.TimeoutError: If timeout is reached.
        """
        queue = self._queues.setdefault(agent_name, asyncio.Queue())
        if timeout:
            return await asyncio.wait_for(queue.get(), timeout=timeout)
        return await queue.get()
