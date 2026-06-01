# coding: utf-8
"""Runner — the global execution entry point for jiuwen.

The Runner provides:
- ResourceManager: process-global registry for workflows, tools, agents
- run_agent(): unified async entry point for executing agents
"""

from typing import Any, Callable

from jiuwen.core.session import Session
from jiuwen.core.workflow import Workflow, generate_workflow_key


class ResourceManager:
    """Process-global registry for jiuwen resources.

    Manages workflows, tools, and agents by stable string keys.
    Workflows are stored as factory functions (lazy instantiation).
    """

    def __init__(self):
        self._workflows: dict[str, Callable[[], Workflow]] = {}
        self._tools: dict[str, Any] = {}

    def add_workflow(self, key: str, factory: Callable[[], Workflow]) -> None:
        """Register a workflow factory under the given key.

        Args:
            key: Stable identifier (typically from generate_workflow_key).
            factory: Zero-argument callable that returns a Workflow instance.
        """
        self._workflows[key] = factory

    def get_workflow(self, key: str) -> Workflow | None:
        """Get a workflow instance by key.

        Args:
            key: The workflow key to look up.

        Returns:
            The Workflow instance, or None if not found.
        """
        factory = self._workflows.get(key)
        if factory:
            return factory()
        return None

    def add_tool(self, key: str, tool: Any) -> None:
        """Register a tool under the given key."""
        self._tools[key] = tool

    def get_tool(self, key: str) -> Any | None:
        """Get a tool by key."""
        return self._tools.get(key)


class Runner:
    """Global entry point for executing agents.

    Usage::

        # Register workflows
        Runner.resource_mgr.add_workflow("my_wf_1.0", lambda: create_my_wf())

        # Run an agent
        result = await Runner.run_agent(agent, {"query": "hello"})
    """

    resource_mgr: ResourceManager = ResourceManager()

    @classmethod
    async def run_agent(
        cls, agent: Any, inputs: dict[str, Any], session: Session | None = None
    ) -> dict[str, Any]:
        """Execute an agent with the given inputs.

        Args:
            agent: An agent instance (WorkflowAgent or ReActAgent).
            inputs: Input data for the agent.
            session: Optional session for multi-turn conversations.

        Returns:
            Dict with agent results.
        """
        return await agent.run(inputs, session=session) if session else await agent.run(inputs)
