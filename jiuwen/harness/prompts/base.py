# coding: utf-8
"""BaseSection — abstract base for prompt sections."""

from abc import ABC, abstractmethod
from typing import Any


class BaseSection(ABC):
    """Abstract base for a prompt section.

    Each section produces a portion of the system prompt.
    Sections are composable via PromptBuilder.

    Usage::

        class CustomSection(BaseSection):
            def build(self, context):
                return "Custom instructions here."
    """

    @abstractmethod
    def build(self, context: dict[str, Any]) -> str:
        """Build this section's contribution to the system prompt.

        Args:
            context: Dict with contextual info (workspace, tools, etc.)

        Returns:
            A string to include in the system prompt.
        """
        ...
