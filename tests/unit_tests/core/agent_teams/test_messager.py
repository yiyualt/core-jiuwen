# coding: utf-8
"""Tests for InProcessMessager, Schema, and Spawner."""

import asyncio
import pytest
from jiuwen.core.agent_teams.messager import InProcessMessager
from jiuwen.core.agent_teams.schema import TeamEvent, TaskBlueprint
from jiuwen.core.agent_teams.spawn import AgentSpawner


class TestInProcessMessager:
    @pytest.mark.asyncio
    async def test_send_receive(self):
        msgr = InProcessMessager()
        await msgr.send("agent_b", {"msg": "hello"})
        msg = await msgr.receive("agent_b")
        assert msg == {"msg": "hello"}

    @pytest.mark.asyncio
    async def test_timeout(self):
        msgr = InProcessMessager()
        with pytest.raises(asyncio.TimeoutError):
            await msgr.receive("nobody", timeout=0.01)

    @pytest.mark.asyncio
    async def test_multiple_agents(self):
        msgr = InProcessMessager()
        await msgr.send("a", {"n": 1})
        await msgr.send("b", {"n": 2})
        assert (await msgr.receive("a")) == {"n": 1}
        assert (await msgr.receive("b")) == {"n": 2}


class TestSchema:
    def test_team_event(self):
        e = TeamEvent(type="task_assigned", source="coordinator", target="coder", data={"task": "fix bug"})
        assert e.type == "task_assigned"
        assert e.target == "coder"

    def test_task_blueprint_lifecycle(self):
        t = TaskBlueprint(task_id="t1", description="fix bug")
        assert t.status == "pending"
        t.mark_running()
        assert t.status == "running"
        t.mark_done({"result": "fixed"})
        assert t.status == "done"
        assert t.result == {"result": "fixed"}


class TestSpawner:
    @pytest.mark.asyncio
    async def test_spawn_agent(self):
        from tests.conftest import FakeLLMClient
        from jiuwen.core.single_agent.agents import ReActAgent

        client = FakeLLMClient(["ok"])
        spawner = AgentSpawner()
        agent = spawner.spawn("coder", lambda: ReActAgent(client=client))
        assert "coder" in spawner.agents
        assert agent is not None

    def test_duplicate_raises(self):
        spawner = AgentSpawner()
        spawner.spawn("x", lambda: None)
        with pytest.raises(ValueError):
            spawner.spawn("x", lambda: None)

    def test_shared_messager(self):
        msgr = InProcessMessager()
        spawner = AgentSpawner(messager=msgr)
        spawner.spawn("a", lambda: None)
        spawner.messager is msgr
