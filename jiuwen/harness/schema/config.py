# coding: utf-8
"""DeepAgentConfig — configuration for a coding agent."""

from pydantic import BaseModel

from jiuwen.core.foundation.llm import OpenAIClient


_DEFAULT_SYSTEM_PROMPT = """You are an expert software engineer. You have access to coding tools:

- bash(command): Run a shell command and get the output
- read(path): Read the contents of a file
- write(path, content): Write content to a file

Use these tools to help users with coding tasks. Think carefully before each action.
When writing code, follow best practices: clear naming, error handling, and tests."""


class DeepAgentConfig(BaseModel):
    """Configuration for a DeepAgent coding agent.

    Attributes:
        client: LLM client for reasoning (defaults to OpenAIClient.from_env()).
        workspace_dir: Root directory for file operations.
        system_prompt: System prompt for the agent.
        max_iterations: Maximum number of tool-calling cycles.
    """

    workspace_dir: str = "."
    system_prompt: str = _DEFAULT_SYSTEM_PROMPT
    max_iterations: int = 50

    model_config = {"arbitrary_types_allowed": True}
