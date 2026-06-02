# coding: utf-8
"""PromptBuilder — composes multiple sections into a full system prompt."""

from typing import Any

from jiuwen.harness.prompts.base import BaseSection
from jiuwen.harness.prompts.sections import (
    IdentitySection,
    ToolsSection,
    SafetySection,
    WorkspaceSection,
)


class PromptBuilder:
    """Composes multiple prompt sections into a complete system prompt.

    Usage::

        builder = PromptBuilder([
            IdentitySection(),
            ToolsSection(),
            SafetySection(),
        ])
        prompt = builder.build({"workspace": "/project"})
    """

    def __init__(self, sections: list[BaseSection] | None = None):
        self._sections = sections or []

    def add_section(self, section: BaseSection) -> None:
        """Append a section to the builder."""
        self._sections.append(section)

    def build(self, context: dict[str, Any] | None = None) -> str:
        """Build the full system prompt from all sections.

        Args:
            context: Dict passed to each section's build() method.

        Returns:
            Complete system prompt string.
        """
        ctx = context or {}
        parts = []
        for section in self._sections:
            text = section.build(ctx)
            if text:
                parts.append(text)
        return "\n\n".join(parts)


# Default builder used by DeepAgent
default_builder = PromptBuilder([
    IdentitySection(),
    ToolsSection(),
    SafetySection(),
    WorkspaceSection(),
])
