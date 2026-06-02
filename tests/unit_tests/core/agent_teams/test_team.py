# coding: utf-8
"""Tests for Team and CoordinatorAgent."""

import pytest
from tests.conftest import FakeLLMClient
from jiuwen.core.single_agent.agents import ReActAgent
from jiuwen.core.agent_teams.team import Team, CoordinatorAgent


@pytest.fixture
def researcher():
    return ReActAgent(
        client=FakeLLMClient(["AI safety is about preventing harm from AI systems."]),
        system_prompt="You are a researcher.",
    )


@pytest.fixture
def writer():
    return ReActAgent(
        client=FakeLLMClient(["# AI Safety Report\n\nThis report covers..."]),
        system_prompt="You are a technical writer.",
    )


class TestCoordinatorAgent:
    @pytest.mark.asyncio
    async def test_delegate_to_member(self, researcher):
        coordinator = CoordinatorAgent(
            client=FakeLLMClient([
                "Action: delegate(agent_name='researcher', task='research AI')",
                "Final Answer: Research complete.",
            ]),
            members={"researcher": researcher},
        )
        result = await coordinator.run({"query": "Research AI safety"})
        assert "Research complete" in result["result"]

    @pytest.mark.asyncio
    async def test_delegate_unknown_agent(self):
        coordinator = CoordinatorAgent(
            client=FakeLLMClient([
                "Action: delegate(agent_name='unknown', task='do something')",
                "Final Answer: Failed.",
            ]),
            members={},
        )
        result = await coordinator.run({"query": "test"})
        assert "Failed" in result["result"]


class TestTeam:
    @pytest.mark.asyncio
    async def test_two_member_team(self, researcher, writer):
        team = Team(
            members={"researcher": researcher, "writer": writer},
            client=FakeLLMClient([
                "Action: delegate(agent_name='researcher', task='research AI safety')",
                "Thought: got research\nAction: delegate(agent_name='writer', task='write a report about AI safety')",
                "Final Answer: The report has been completed.",
            ]),
        )

        result = await team.run("Research AI safety and write a report")
        assert "completed" in result["result"].lower()

    @pytest.mark.asyncio
    async def test_team_members_property(self, researcher, writer):
        team = Team(
            members={"researcher": researcher, "writer": writer},
            client=FakeLLMClient(["Final Answer: ok"]),
        )
        assert "researcher" in team.members
        assert "writer" in team.members

    @pytest.mark.asyncio
    async def test_single_member_team(self):
        agent = ReActAgent(
            client=FakeLLMClient(["Final Answer: Done."]),
            system_prompt="You are a generalist.",
        )
        team = Team(
            members={"agent": agent},
            client=FakeLLMClient([
                "Action: delegate(agent_name='agent', task='do it')",
                "Final Answer: Done via delegate.",
            ]),
        )
        result = await team.run("Do something")
        assert "Done via delegate" in result["result"]
