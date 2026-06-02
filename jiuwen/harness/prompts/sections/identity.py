# coding: utf-8
"""IdentitySection — defines the agent's role and personality."""

from jiuwen.harness.prompts.base import BaseSection


class IdentitySection(BaseSection):
    """Defines the agent's core identity and behavior."""

    def __init__(self, role: str | None = None):
        self._role = role or "an expert software engineer"

    def build(self, context: dict) -> str:
        return (
            f"You are {self._role}. "
            f"You have access to coding tools that help you read, write, and execute code. "
            f"Think carefully before each action. "
            f"When writing code, follow best practices: clear naming, error handling, and tests."
        )
