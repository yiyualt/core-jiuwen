# coding: utf-8
"""Tests for Session and StreamEmitter."""

import asyncio
import pytest
from jiuwen.core.session import Session, StreamEmitter


class TestSession:
    def test_empty_initially(self):
        s = Session()
        assert len(s) == 0
        assert s.get_messages() == []

    def test_add_messages(self):
        s = Session()
        s.add_message("user", "hello")
        s.add_message("assistant", "hi")
        assert len(s) == 2
        assert s.get_messages()[0] == {"role": "user", "content": "hello"}

    def test_clear(self):
        s = Session()
        s.add_message("user", "hello")
        s.clear()
        assert len(s) == 0

    def test_state(self):
        s = Session()
        s.set_state("name", "Bob")
        assert s.get_state("name") == "Bob"
        assert s.get_state("missing", "default") == "default"

    def test_get_messages_is_copy(self):
        s = Session()
        s.add_message("user", "hello")
        msgs = s.get_messages()
        msgs.append({"role": "x", "content": "y"})
        assert len(s) == 1  # original unchanged


class TestStreamEmitter:
    @pytest.mark.asyncio
    async def test_emit_and_iterate(self):
        emitter = StreamEmitter()

        async def producer():
            await emitter.emit("a")
            await emitter.emit("b")
            await emitter.close()

        asyncio.create_task(producer())
        results = []
        async for chunk in emitter:
            results.append(chunk)
        assert results == ["a", "b"]

    @pytest.mark.asyncio
    async def test_close_without_data(self):
        emitter = StreamEmitter()
        await emitter.close()
        results = [chunk async for chunk in emitter]
        assert results == []


class TestSessionWithAgent:
    @pytest.mark.asyncio
    async def test_multi_turn(self):
        from tests.conftest import FakeLLMClient
        from jiuwen.core.single_agent.agents import ReActAgent

        client = FakeLLMClient([
            "Final Answer: Nice to meet you, Bob!",
            "Final Answer: Your name is Bob.",
        ])
        agent = ReActAgent(client=client)

        session = Session()
        result1 = await agent.run({"query": "I'm Bob"}, session=session)
        assert "Bob" in result1["result"]

        result2 = await agent.run({"query": "What's my name?"}, session=session)
        assert "Bob" in result2["result"]
        assert len(session) == 4  # 2 user + 2 assistant

    @pytest.mark.asyncio
    async def test_stream_with_session(self):
        from tests.conftest import FakeLLMClient
        from jiuwen.core.single_agent.agents import ReActAgent

        client = FakeLLMClient(["Final Answer: Hello!"])
        agent = ReActAgent(client=client)

        session = Session()
        results = []
        async for chunk in agent.stream({"query": "hi"}, session=session):
            results.append(chunk)
        assert results[-1]["type"] == "final"
        assert len(session) == 2
