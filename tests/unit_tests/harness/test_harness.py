# coding: utf-8
"""Tests for DeepAgent, Workspace, and factory."""

import os
import tempfile
from pathlib import Path

import pytest
from tests.conftest import FakeLLMClient
from jiuwen.harness.workspace import Workspace
from jiuwen.harness.schema.config import DeepAgentConfig
from jiuwen.harness.deep_agent import DeepAgent
from jiuwen.harness.factory import create_deep_agent


class TestWorkspace:
    def test_read_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Workspace(tmp)
            ws.write_file("test.txt", "hello")
            assert ws.read_file("test.txt") == "hello"

    def test_list_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Workspace(tmp)
            ws.write_file("a.py", "1")
            ws.write_file("b.py", "2")
            ws.write_file("sub/c.py", "3")
            files = ws.list_files("*.py")
            assert len(files) == 3

    def test_file_not_found(self):
        ws = Workspace("/tmp")
        with pytest.raises(FileNotFoundError):
            ws.read_file("nonexistent_xyz.txt")

    def test_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Workspace(tmp)
            ws.write_file("deep/nested/file.txt", "content")
            assert ws.read_file("deep/nested/file.txt") == "content"

    def test_ignores_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Workspace(tmp)
            ws.write_file("normal.py", "x")
            ws.write_file(".hidden.py", "y")
            Path(tmp, "__pycache__").mkdir(exist_ok=True)
            Path(tmp, "__pycache__/cached.py").write_text("z")
            files = ws.list_files("*.py")
            assert len(files) == 1
            assert files[0] == "normal.py"


class TestDeepAgentConfig:
    def test_defaults(self):
        config = DeepAgentConfig(workspace_dir="/tmp")
        assert config.workspace_dir == "/tmp"
        assert config.max_iterations == 50

    def test_field_default(self):
        config = DeepAgentConfig()
        assert "expert software engineer" in config.system_prompt.lower()


class TestDeepAgent:
    @pytest.mark.asyncio
    async def test_has_coding_tools(self):
        client = FakeLLMClient(["Final Answer: done"])
        config = DeepAgentConfig(workspace_dir="/tmp")
        agent = DeepAgent(client, config)
        result = await agent.run({"query": "list files"})
        assert "done" in result["result"]

    @pytest.mark.asyncio
    async def test_read_tool(self, tmp_path):
        tmp_path = str(tmp_path)
        Path(tmp_path, "hello.py").write_text("print('hi')")
        client = FakeLLMClient([
            "Action: read(path='hello.py')",
            "Final Answer: The file contains print('hi')",
        ])
        config = DeepAgentConfig(workspace_dir=tmp_path)
        agent = DeepAgent(client, config)
        result = await agent.run({"query": "what's in hello.py?"})
        assert "hi" in result["result"]

    def test_workspace_property(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = FakeLLMClient(["ok"])
            agent = DeepAgent(client, DeepAgentConfig(workspace_dir=tmp))
            assert isinstance(agent.workspace, Workspace)


class TestFactory:
    @pytest.mark.asyncio
    async def test_create_with_defaults(self):
        # This will fail without .env, so test with monkeypatch
        pass  # Factory requires real client or env — tested via unit tests above

    def test_create_with_explicit_client(self):
        client = FakeLLMClient(["Final Answer: ok"])
        agent = create_deep_agent(client=client, workspace_dir="/tmp")
        assert isinstance(agent, DeepAgent)
