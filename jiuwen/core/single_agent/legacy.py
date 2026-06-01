# coding: utf-8
"""WorkflowAgent — an AI agent that executes workflows.

The WorkflowAgent is the primary user-facing abstraction for running
workflows. Users configure an agent, bind workflows to it, and run
it through the Runner.
"""

from typing import Any

from pydantic import BaseModel, Field

from jiuwen.core.common import BaseCard
from jiuwen.core.workflow import Workflow, generate_workflow_key


class AgentCard(BaseCard):
    """Metadata card describing an AI agent.

    Attributes:
        version: Agent version string.
        model: Default model for this agent (e.g., "gpt-4o").
    """

    version: str = ""
    model: str = ""


class WorkflowAgentConfig(BaseModel):
    """Runtime configuration for a WorkflowAgent.

    Attributes:
        id: Unique identifier for this agent instance.
        version: Agent version.
        description: Human-readable description.
    """

    id: str = ""
    version: str = "0.1.0"
    description: str = ""


class WorkflowAgent:
    """An AI agent that executes one or more workflows.

    Usage::

        # Create agent
        config = WorkflowAgentConfig(id="assistant", version="0.1")
        agent = WorkflowAgent(config)

        # Bind a workflow
        flow = Workflow(...)
        flow.set_start_comp("start", Start())...
        agent.add_workflows([flow])

        # Run via Runner
        result = await Runner.run_agent(agent, {"query": "hello"})

        # Or run directly
        result = await agent.run({"query": "hello"})
    """

    def __init__(self, config: WorkflowAgentConfig):
        self._config = config
        self._workflows: list[Workflow] = []

    @property
    def config(self) -> WorkflowAgentConfig:
        return self._config

    def add_workflows(self, workflows: list[Workflow]) -> None:
        """Bind one or more workflows to this agent.

        Args:
            workflows: List of Workflow instances to add.
        """
        self._workflows.extend(workflows)

    async def run(self, inputs: dict[str, Any], session: Any = None) -> dict[str, Any]:
        """Execute the agent's workflows with the given inputs.

        If multiple workflows are bound, runs them sequentially and
        returns combined results keyed by workflow card id.

        Args:
            inputs: Input data passed to each workflow's invoke().
            session: Optional session (for compatibility with Runner).

        Returns:
            Dict with workflow results. For single workflow, returns
            the workflow output directly. For multiple, keys are
            workflow card ids.
        """
        if not self._workflows:
            raise ValueError("No workflows bound to agent. Call add_workflows() first.")

        results: dict[str, Any] = {}
        for wf in self._workflows:
            output = await wf.invoke(inputs)
            key = generate_workflow_key(wf.card.id, wf.card.version)
            results[key] = output.result

        if len(results) == 1:
            return {"result": list(results.values())[0]}
        return {"results": results}
