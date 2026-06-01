# coding: utf-8
"""Single agent — agent abstractions for jiuwen.

Provides:
- AgentCard: metadata describing an AI agent
- WorkflowAgentConfig: runtime configuration for workflow-based agents
- WorkflowAgent: agent that executes workflows
"""

from jiuwen.core.single_agent.legacy import AgentCard, WorkflowAgentConfig, WorkflowAgent

__all__ = ["AgentCard", "WorkflowAgentConfig", "WorkflowAgent"]
