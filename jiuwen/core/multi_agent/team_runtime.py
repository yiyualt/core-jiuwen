# coding: utf-8
"""TeamRuntime — manages agent lifecycle and task routing."""

from typing import Any

from jiuwen.core.multi_agent.message_bus import MessageBus


class TeamRuntime:
    """Dynamic team runtime with agent registry and task routing.

    Usage::

        rt = TeamRuntime()
        rt.register("coder", agent, capabilities=["python", "debug"])
        rt.register("writer", agent, capabilities=["docs", "blog"])

        best = rt.route("fix python bug")  # → "coder"
        best = rt.route("write blog post")  # → "writer"
    """

    def __init__(self, bus: MessageBus | None = None):
        self._bus = bus or MessageBus()
        self._agents: dict[str, Any] = {}
        self._capabilities: dict[str, list[str]] = {}

    @property
    def bus(self) -> MessageBus:
        return self._bus

    @property
    def agents(self) -> dict[str, Any]:
        return dict(self._agents)

    def register(self, name: str, agent: Any, capabilities: list[str] | None = None) -> None:
        """Register an agent with its capabilities.

        Args:
            name: Agent name.
            agent: Agent instance.
            capabilities: List of capability tags for task routing.

        Raises:
            ValueError: If name already registered.
        """
        if name in self._agents:
            raise ValueError(f"Agent '{name}' already registered")
        self._agents[name] = agent
        self._capabilities[name] = capabilities or []

    def unregister(self, name: str) -> None:
        """Remove an agent from the runtime."""
        self._agents.pop(name, None)
        self._capabilities.pop(name, None)

    def route(self, task: str) -> str | None:
        """Find the best agent for a task based on capability keywords.

        Args:
            task: Task description string.

        Returns:
            Agent name with the most matching capabilities, or None if no match.
        """
        task_lower = task.lower()
        best_name = None
        best_score = 0
        for name, caps in self._capabilities.items():
            score = sum(1 for cap in caps if cap.lower() in task_lower)
            if score > best_score:
                best_score = score
                best_name = name
        return best_name

    async def broadcast(self, topic: str, message: dict) -> None:
        """Publish a message to all registered agents."""
        await self._bus.publish(topic, message)
