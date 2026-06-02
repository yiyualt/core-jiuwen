# coding: utf-8
"""SafetySection — safety rules for the coding agent."""

from jiuwen.harness.prompts.base import BaseSection


class SafetySection(BaseSection):
    """Adds safety guidelines to the system prompt."""

    def build(self, context: dict) -> str:
        return (
            "Safety rules:\n"
            "- Never delete files without explicit user confirmation.\n"
            "- Never run destructive commands (rm -rf, format, etc.) without asking.\n"
            "- Never modify files outside the workspace directory.\n"
            "- If a command produces an error, analyze it before retrying.\n"
            "- When uncertain, ask the user for clarification rather than guessing."
        )
