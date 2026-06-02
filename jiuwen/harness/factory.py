# coding: utf-8
"""Factory function for creating DeepAgent instances with sensible defaults."""

from jiuwen.core.foundation.llm import LLMClient, OpenAIClient
from jiuwen.harness.deep_agent import DeepAgent
from jiuwen.harness.schema.config import DeepAgentConfig


def create_deep_agent(
    client: LLMClient | None = None,
    workspace_dir: str = ".",
    system_prompt: str | None = None,
    max_iterations: int = 50,
) -> DeepAgent:
    """Create a DeepAgent with sensible defaults.

    Args:
        client: LLM client. If None, uses OpenAIClient.from_env().
        workspace_dir: Root directory for file operations.
        system_prompt: Custom system prompt. If None, uses default coding prompt.
        max_iterations: Maximum tool-calling cycles.

    Returns:
        Configured DeepAgent instance.

    Usage::

        # Simplest: auto-configure from .env
        agent = create_deep_agent()

        # Custom workspace
        agent = create_deep_agent(workspace_dir="/path/to/project")

        # Full control
        from jiuwen.core.foundation import OpenAIClient
        agent = create_deep_agent(
            client=OpenAIClient.from_env(),
            workspace_dir="./my-app",
            system_prompt="You are a Python expert.",
        )
    """
    resolved_client = client or OpenAIClient.from_env()

    config = DeepAgentConfig(
        workspace_dir=workspace_dir,
        system_prompt=system_prompt or DeepAgentConfig.model_fields["system_prompt"].default,
        max_iterations=max_iterations,
    )
    return DeepAgent(resolved_client, config)
