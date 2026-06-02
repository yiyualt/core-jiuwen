# coding: utf-8
"""DeepAgent — a coding agent with built-in tools and system prompt."""

from pathlib import Path

from jiuwen.core.foundation.llm import LLMClient
from jiuwen.core.foundation.tool import ToolCard
from jiuwen.core.single_agent.agents import ReActAgent
from jiuwen.harness.schema.config import DeepAgentConfig
from jiuwen.harness.workspace import Workspace


class DeepAgent(ReActAgent):
    """A coding agent with built-in bash, read, and write tools.

    DeepAgent extends ReActAgent with coding-specific tools that
    operate on a workspace directory. It is the primary agent
    for software engineering tasks.

    Usage::

        from jiuwen.harness import DeepAgent, DeepAgentConfig
        from jiuwen.core.foundation import OpenAIClient

        client = OpenAIClient.from_env()
        agent = DeepAgent(client, DeepAgentConfig(workspace_dir="/path/to/project"))
        result = await agent.run({"query": "Fix the bug in main.py"})
    """

    def __init__(self, client: LLMClient, config: DeepAgentConfig):
        self._config = config
        self._client = client
        self._workspace = Workspace(config.workspace_dir)

        tools = [
            self._make_bash_tool(),
            self._make_read_tool(),
            self._make_write_tool(),
        ]

        super().__init__(
            client=self._client,
            tools=tools,
            system_prompt=config.system_prompt,
            max_iterations=config.max_iterations,
        )

    @property
    def workspace(self) -> Workspace:
        return self._workspace

    @property
    def config(self) -> DeepAgentConfig:
        return self._config

    def _make_bash_tool(self) -> ToolCard:
        async def bash(command: str) -> str:
            import subprocess
            import asyncio
            try:
                proc = await asyncio.create_subprocess_shell(
                    command,
                    cwd=str(self._workspace.root),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=30
                )
                result = stdout.decode("utf-8", errors="replace")
                if stderr:
                    result += "\n[stderr]\n" + stderr.decode("utf-8", errors="replace")
                return result.strip() or "(no output)"
            except asyncio.TimeoutError:
                return "Error: command timed out (30s)"
            except Exception as e:
                return f"Error: {e}"

        return ToolCard(
            name="bash",
            description="Run a shell command and return its output",
            parameters={
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Shell command to execute"}},
                "required": ["command"],
            },
            func=bash,
        )

    def _make_read_tool(self) -> ToolCard:
        async def read(path: str) -> str:
            try:
                return self._workspace.read_file(path)
            except FileNotFoundError:
                return f"Error: file not found: {path}"
            except Exception as e:
                return f"Error reading file: {e}"

        return ToolCard(
            name="read",
            description="Read the contents of a file",
            parameters={
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Relative path to the file"}},
                "required": ["path"],
            },
            func=read,
        )

    def _make_write_tool(self) -> ToolCard:
        async def write(path: str, content: str) -> str:
            try:
                self._workspace.write_file(path, content)
                return f"Successfully wrote {len(content)} bytes to {path}"
            except ValueError as e:
                return f"Error: {e}"
            except Exception as e:
                return f"Error writing file: {e}"

        return ToolCard(
            name="write",
            description="Write content to a file (creates parent directories if needed)",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to the file"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
            func=write,
        )
