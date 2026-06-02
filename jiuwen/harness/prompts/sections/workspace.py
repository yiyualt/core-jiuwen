# coding: utf-8
"""WorkspaceSection — provides workspace directory context."""

from jiuwen.harness.prompts.base import BaseSection


class WorkspaceSection(BaseSection):
    """Informs the agent about its working directory."""

    def build(self, context: dict) -> str:
        workspace = context.get("workspace", "current directory")
        return (
            f"Workspace: {workspace}\n"
            f"All file paths are relative to this directory. "
            f"Use 'bash' with commands like 'ls' or 'find' to explore the project structure."
        )
