# coding: utf-8
"""ToolsSection — describes available tools and usage format."""

from jiuwen.harness.prompts.base import BaseSection


class ToolsSection(BaseSection):
    """Describes the available coding tools and how to use them."""

    def build(self, context: dict) -> str:
        return (
            "Available tools:\n"
            "- bash(command: str): Run a shell command and get the output. "
            "Use for running code, installing packages, git operations, and file searching.\n"
            "- read(path: str): Read the contents of a file. "
            "Use before editing to understand the current code.\n"
            "- write(path: str, content: str): Write content to a file. "
            "Creates parent directories if needed. Use to create or modify files.\n\n"
            "Use these tools with the standard Thought/Action/Observation format. "
            "Execute one action at a time and observe results before proceeding."
        )
