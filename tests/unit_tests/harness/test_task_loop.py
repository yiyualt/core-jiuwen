# coding: utf-8
"""Tests for TaskEvent, EventHandler, TaskExecutor, and LoopCoordinator."""

import asyncio
import pytest
from tests.conftest import FakeLLMClient
from jiuwen.core.single_agent.agents import ReActAgent
from jiuwen.harness.task_loop.events import TaskEvent
from jiuwen.harness.task_loop.handler import EventHandler
from jiuwen.harness.task_loop.executor import TaskExecutor
from jiuwen.harness.task_loop.coordinator import LoopCoordinator


class TestTaskEvent:
    def test_creation(self):
        event = TaskEvent(type="task_start", data={"task": "test"})
        assert event.type == "task_start"
        assert event.data == {"task": "test"}
        assert event.timestamp > 0

    def test_default_data(self):
        event = TaskEvent(type="ping")
        assert event.data == {}


class TestEventHandler:
    @pytest.mark.asyncio
    async def test_collecting_handler(self):
        class CollectHandler(EventHandler):
            def __init__(self):
                self.events = []

            async def on_event(self, event):
                self.events.append(event)

        handler = CollectHandler()
        await handler.on_event(TaskEvent(type="test"))
        assert len(handler.events) == 1
        assert handler.events[0].type == "test"


class TestTaskExecutor:
    @pytest.mark.asyncio
    async def test_emits_events(self):
        class CollectHandler(EventHandler):
            def __init__(self):
                self.events = []

            async def on_event(self, event):
                self.events.append(event)

        agent = ReActAgent(client=FakeLLMClient(["Final Answer: done"]))
        handler = CollectHandler()
        executor = TaskExecutor(agent, handlers=[handler])

        result = await executor.execute("test task")
        assert result["result"] == "done"
        assert len(handler.events) == 2
        assert handler.events[0].type == "task_start"
        assert handler.events[1].type == "task_complete"

    @pytest.mark.asyncio
    async def test_emits_error(self):
        class CollectHandler(EventHandler):
            def __init__(self):
                self.events = []

            async def on_event(self, event):
                self.events.append(event)

        class BrokenAgent:
            async def run(self, inputs, session=None):
                raise ValueError("fail")

        handler = CollectHandler()
        executor = TaskExecutor(BrokenAgent(), handlers=[handler])

        with pytest.raises(ValueError):
            await executor.execute("task")
        assert handler.events[0].type == "task_start"
        assert handler.events[1].type == "error"


class TestLoopCoordinator:
    @pytest.mark.asyncio
    async def test_processes_tasks(self):
        class CollectHandler(EventHandler):
            def __init__(self):
                self.events = []

            async def on_event(self, event):
                self.events.append(event)

        agent = ReActAgent(client=FakeLLMClient(["Final Answer: ok"]))
        handler = CollectHandler()
        executor = TaskExecutor(agent, handlers=[handler])
        coordinator = LoopCoordinator(executor)

        await coordinator.submit("task A")
        await coordinator.submit("task B")
        await coordinator.submit(None)

        await coordinator.run()
        assert len(handler.events) == 4  # 2 tasks × 2 events
        assert handler.events[0].data["task"] == "task A"
        assert handler.events[2].data["task"] == "task B"
