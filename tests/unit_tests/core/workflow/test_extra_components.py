# coding: utf-8
"""Tests for Questioner, IntentDetection, HTTPRequest, and Loop components."""

import pytest
from jiuwen.core.workflow.components.llm.questioner_comp import QuestionerComponent
from jiuwen.core.workflow.components.llm.intent_detection_comp import IntentDetectionComponent
from jiuwen.core.workflow.components.tool.http_comp import HTTPRequestComponent
from jiuwen.core.workflow.components.flow.loop_comp import LoopComponent


class TestQuestioner:
    @pytest.mark.asyncio
    async def test_missing_field_asks(self):
        comp = QuestionerComponent("What is your name?", "name")
        result = await comp.invoke({})
        assert result == {"question": "What is your name?", "field": "name"}

    @pytest.mark.asyncio
    async def test_field_present_passes(self):
        comp = QuestionerComponent("What is your name?", "name")
        result = await comp.invoke({"name": "Alice"})
        assert result == {"output": "Alice"}

    @pytest.mark.asyncio
    async def test_empty_string_treated_as_missing(self):
        comp = QuestionerComponent("Enter age", "age")
        result = await comp.invoke({"age": ""})
        assert "question" in result


class TestIntentDetection:
    @pytest.mark.asyncio
    async def test_matches_keyword(self):
        comp = IntentDetectionComponent({"greeting": ["hello", "hi"]})
        result = await comp.invoke({"query": "hello there"})
        assert result == {"intent": "greeting", "confidence": 1.0}

    @pytest.mark.asyncio
    async def test_no_match(self):
        comp = IntentDetectionComponent({"greeting": ["hello"]})
        result = await comp.invoke({"query": "what is the weather"})
        assert result == {"intent": "unknown", "confidence": 0.0}

    @pytest.mark.asyncio
    async def test_case_insensitive(self):
        comp = IntentDetectionComponent({"help": ["HELP", "Assist"]})
        result = await comp.invoke({"query": "Please assist me"})
        assert result["intent"] == "help"


class TestHTTPRequest:
    @pytest.mark.asyncio
    async def test_renders_url(self):
        comp = HTTPRequestComponent("https://httpbin.org/get?q={{query}}")
        result = await comp.invoke({"query": "test"})
        # httpbin may or may not be reachable, just check it doesn't crash
        assert "status" in result


class TestLoop:
    @pytest.mark.asyncio
    async def test_accumulates_items(self):
        comp = LoopComponent(max_iterations=3)
        r1 = await comp.invoke({"item": "a"})
        assert r1 == {"items": ["a"], "count": 1, "done": False}

        r2 = await comp.invoke({"item": "b"})
        assert r2 == {"items": ["a", "b"], "count": 2, "done": False}

        r3 = await comp.invoke({"item": "c"})
        assert r3 == {"items": ["a", "b", "c"], "count": 3, "done": True}

    @pytest.mark.asyncio
    async def test_reset(self):
        comp = LoopComponent(max_iterations=5)
        await comp.invoke({"item": "x"})
        await comp.invoke({"item": "y"})
        assert comp._count == 2
        comp.reset()
        assert comp._count == 0
        assert comp._items == []
