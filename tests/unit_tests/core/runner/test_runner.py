# coding: utf-8
"""Tests for Runner and ResourceManager."""

import pytest
from jiuwen.core.runner.runner import Runner, ResourceManager
from jiuwen.core.workflow import Workflow, Start, End


class TestResourceManager:
    def test_register_and_get_workflow(self):
        mgr = ResourceManager()
        wf = Workflow()
        wf.set_start_comp("s", Start())
        wf.set_end_comp("e", End())
        wf.add_connection("s", "e")
        mgr.add_workflow("test_1.0", lambda: wf)
        result = mgr.get_workflow("test_1.0")
        assert result is wf

    def test_get_missing_returns_none(self):
        mgr = ResourceManager()
        assert mgr.get_workflow("nonexistent") is None

    def test_add_tool(self):
        mgr = ResourceManager()
        mgr.add_tool("search", {"name": "search"})
        assert mgr.get_tool("search") == {"name": "search"}


class TestRunner:
    @pytest.mark.asyncio
    async def test_run_agent(self):
        from jiuwen.core.single_agent import WorkflowAgentConfig, WorkflowAgent

        wf = Workflow()
        wf.set_start_comp("s", Start())
        wf.set_end_comp("e", End())
        wf.add_connection("s", "e")

        config = WorkflowAgentConfig(id="test_agent")
        agent = WorkflowAgent(config)
        agent.add_workflows([wf])

        result = await Runner.run_agent(agent, {"val": "hello"})
        assert "result" in result

    @pytest.mark.asyncio
    async def test_resource_mgr_integration(self):
        from jiuwen.core.single_agent import WorkflowAgentConfig, WorkflowAgent

        wf = Workflow()
        wf.set_start_comp("s", Start())
        wf.set_end_comp("e", End())
        wf.add_connection("s", "e")

        Runner.resource_mgr.add_workflow("my_agent_1.0", lambda: wf)

        retrieved = Runner.resource_mgr.get_workflow("my_agent_1.0")
        assert retrieved is not None

        config = WorkflowAgentConfig(id="my_agent")
        agent = WorkflowAgent(config)
        agent.add_workflows([retrieved])

        result = await Runner.run_agent(agent, {"msg": "hi"})
        assert "result" in result
