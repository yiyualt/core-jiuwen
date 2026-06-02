# coding: utf-8
"""AgentSpawner — creates and manages child agents."""

from typing import Any, Callable

from jiuwen.core.agent_teams.messager import InProcessMessager


class AgentSpawner:
    """Creates child agents with shared messaging and resources.

    Usage::

        msgr = InProcessMessager()
        spawner = AgentSpawner(messager=msgr)

        agent = spawner.spawn(
            "coder",
            lambda: ReActAgent(client, tools=[...]),
        )
        # agent is now registered and can receive messages via msgr
    """

    def __init__(self, messager: InProcessMessager | None = None):
        self._messager = messager or InProcessMessager()
        self._agents: dict[str, Any] = {}

    @property
    def messager(self) -> InProcessMessager:
        return self._messager

    @property
    def agents(self) -> dict[str, Any]:
        return dict(self._agents)

    def spawn(self, name: str, factory: Callable[[], Any]) -> Any:
        """Create and register a child agent.

        Args:
            name: Unique name for the agent.
            factory: Zero-argument callable that returns an agent instance.

        Returns:
            The created agent.

        Raises:
            ValueError: If an agent with this name already exists.
        """
        if name in self._agents:
            raise ValueError(f"Agent '{name}' already exists")
        agent = factory()
        self._agents[name] = agent
        return agent

    def get(self, name: str) -> Any | None:
        """Get a registered agent by name."""
        return self._agents.get(name)

    def remove(self, name: str) -> None:
        """Remove a registered agent."""
        self._agents.pop(name, None)
