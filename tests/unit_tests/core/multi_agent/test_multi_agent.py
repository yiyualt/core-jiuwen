# coding: utf-8
"""Tests for MessageBus, TeamRuntime, and handoff."""

import pytest
from jiuwen.core.multi_agent import MessageBus, TeamRuntime, handoff


class TestMessageBus:
    @pytest.mark.asyncio
    async def test_publish_subscribe(self):
        bus = MessageBus()
        received = []

        async def handler(msg):
            received.append(msg)

        bus.subscribe("tasks", handler)
        await bus.publish("tasks", {"id": 1})
        assert len(received) == 1
        assert received[0] == {"id": 1}

    @pytest.mark.asyncio
    async def test_multiple_handlers(self):
        bus = MessageBus()
        results = []

        async def h1(msg):
            results.append(("h1", msg))

        async def h2(msg):
            results.append(("h2", msg))

        bus.subscribe("x", h1)
        bus.subscribe("x", h2)
        await bus.publish("x", {"data": "test"})
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        bus = MessageBus()
        received = []

        async def handler(msg):
            received.append(msg)

        bus.subscribe("t", handler)
        bus.unsubscribe("t", handler)
        await bus.publish("t", {"x": 1})
        assert len(received) == 0


class TestTeamRuntime:
    def test_routing(self):
        rt = TeamRuntime()
        rt.register("coder", None, capabilities=["python", "debug"])
        rt.register("writer", None, capabilities=["docs", "blog"])

        assert rt.route("fix python bug in main.py") == "coder"
        assert rt.route("write a blog post about AI") == "writer"
        assert rt.route("make coffee") is None

    def test_duplicate_raises(self):
        rt = TeamRuntime()
        rt.register("a", None)
        with pytest.raises(ValueError):
            rt.register("a", None)

    def test_unregister(self):
        rt = TeamRuntime()
        rt.register("x", None, capabilities=["test"])
        rt.unregister("x")
        assert "x" not in rt.agents


class TestHandoff:
    @pytest.mark.asyncio
    async def test_handoff(self):
        class FakeAgent:
            async def run(self, inputs, session=None):
                return {"result": f"processed: {inputs['query']}"}

        src = FakeAgent()
        tgt = FakeAgent()
        result = await handoff(src, tgt, "fix the bug")
        assert "processed" in result["result"]
