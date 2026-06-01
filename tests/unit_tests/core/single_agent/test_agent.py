# coding: utf-8
"""Tests for AgentCard, WorkflowAgentConfig, and WorkflowAgent."""

import pytest
from jiuwen.core.common import BaseCard
from jiuwen.core.single_agent.legacy import (
    AgentCard,
    WorkflowAgentConfig,
    WorkflowAgent,
)
from jiuwen.core.workflow import Workflow, Start, End


class TestAgentCard:
    def test_inherits_base_card(self):
        assert isinstance(AgentCard(), BaseCard)

    def test_defaults(self):
        card = AgentCard()
        assert card.version == ""
        assert card.model == ""

    def test_full_construction(self):
        card = AgentCard(
            id="agent-1", name="assistant",
            version="0.1.0", model="gpt-4o",
            description="A helpful assistant",
        )
        assert card.id == "agent-1"
        assert card.model == "gpt-4o"
        assert card.version == "0.1.0"


class TestWorkflowAgentConfig:
    def test_defaults(self):
        config = WorkflowAgentConfig()
        assert config.id == ""
        assert config.version == "0.1.0"

    def test_full(self):
        config = WorkflowAgentConfig(
            id="my_agent", version="2.0", description="My agent"
        )
        assert config.id == "my_agent"


class TestWorkflowAgent:
    @pytest.mark.asyncio
    async def test_run_single_workflow(self):
        wf = Workflow()
        wf.set_start_comp("s", Start())
        wf.set_end_comp("e", End())
        wf.add_connection("s", "e")

        config = WorkflowAgentConfig(id="test")
        agent = WorkflowAgent(config)
        agent.add_workflows([wf])

        result = await agent.run({"msg": "hello"})
        assert "result" in result

    @pytest.mark.asyncio
    async def test_no_workflows_raises(self):
        agent = WorkflowAgent(WorkflowAgentConfig(id="empty"))
        with pytest.raises(ValueError, match="No workflows"):
            await agent.run({})

    @pytest.mark.asyncio
    async def test_multiple_workflows(self):
        wf1 = Workflow()
        wf1.set_start_comp("s1", Start())
        wf1.set_end_comp("e1", End())
        wf1.add_connection("s1", "e1")

        wf2 = Workflow()
        wf2.set_start_comp("s2", Start())
        wf2.set_end_comp("e2", End())
        wf2.add_connection("s2", "e2")

        agent = WorkflowAgent(WorkflowAgentConfig(id="multi"))
        agent.add_workflows([wf1, wf2])

        result = await agent.run({"x": "y"})
        assert "results" in result

    def test_config_property(self):
        config = WorkflowAgentConfig(id="test", version="1.0")
        agent = WorkflowAgent(config)
        assert agent.config.id == "test"
