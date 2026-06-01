# coding: utf-8
"""Tests for ToolCard and ToolComponent."""

import pytest
from jiuwen.core.foundation.tool import ToolCard, ToolComponent
from jiuwen.core.common import BaseCard


class TestToolCard:
    def test_inherits_base_card(self):
        assert isinstance(ToolCard(), BaseCard)

    def test_defaults(self):
        card = ToolCard()
        assert card.parameters is None
        assert card.func is None

    def test_full_construction(self):
        def my_func(x):
            return x

        card = ToolCard(
            id="t1", name="search", description="Search web",
            parameters={"type": "object"}, func=my_func,
        )
        assert card.name == "search"
        assert card.parameters == {"type": "object"}
        assert card.func is my_func

    def test_tool_info(self):
        card = ToolCard(name="search", description="Search", parameters={"q": {"type": "string"}})
        info = card.tool_info()
        assert info["name"] == "search"
        assert info["parameters"] == {"q": {"type": "string"}}

    def test_func_excluded_from_serialization(self):
        card = ToolCard(name="test", func=lambda x: x)
        data = card.model_dump()
        assert "func" not in data
        assert data["name"] == "test"


class TestToolComponent:
    @pytest.mark.asyncio
    async def test_invoke_sync_function(self):
        def add(a: int, b: int) -> int:
            return a + b

        card = ToolCard(name="adder", func=add)
        comp = ToolComponent(card)
        result = await comp.invoke({"a": 3, "b": 4})
        assert result == {"output": 7}

    @pytest.mark.asyncio
    async def test_invoke_async_function(self):
        async def fetch(x: str) -> str:
            return f"got {x}"

        card = ToolCard(name="fetcher", func=fetch)
        comp = ToolComponent(card)
        result = await comp.invoke({"x": "data"})
        assert result == {"output": "got data"}

    @pytest.mark.asyncio
    async def test_invoke_no_function_raises(self):
        card = ToolCard(name="empty")
        comp = ToolComponent(card)
        with pytest.raises(ValueError, match="no function"):
            await comp.invoke({})

    def test_card_property(self):
        def f():
            pass
        card = ToolCard(name="test", func=f)
        comp = ToolComponent(card)
        assert comp.card is card


class TestToolComponentIntegration:
    @pytest.mark.asyncio
    async def test_tool_in_workflow(self):
        from jiuwen.core.workflow import Workflow, Start, End

        def square(x: int) -> int:
            return x * x

        card = ToolCard(name="square", description="Square a number", func=square)
        comp = ToolComponent(card)

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("square", comp)
        wf.set_end_comp("end", End({"responseTemplate": "Result: {{output}}"}))
        wf.add_connection("start", "square")
        wf.add_connection("square", "end")

        result = await wf.invoke({"x": 8})
        assert result.state.value == "COMPLETED"

    @pytest.mark.asyncio
    async def test_llm_with_tool_pipeline(self):
        from jiuwen.core.workflow import Workflow, Start, End
        from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig
        from jiuwen.core.foundation import FakeLLMClient, ModelRequestConfig, ModelClientConfig

        def get_weather(city: str) -> str:
            return f"Weather in {city}: sunny, 25C"

        tool_card = ToolCard(
            name="get_weather",
            description="Get weather for a city",
            parameters={"city": {"type": "string"}},
            func=get_weather,
        )

        llm_config = LLMCompConfig(
            model_client_config=ModelClientConfig(provider="test"),
            model_config=ModelRequestConfig(model="test"),
            template_content=[{"role": "user", "content": "Check the weather in {{city}}"}],
        )
        llm_client = FakeLLMClient(["It is sunny and 25C."])

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("weather_tool", ToolComponent(tool_card))
        wf.add_workflow_comp("llm", LLMComponent(llm_config, llm_client))
        wf.set_end_comp("end", End({"responseTemplate": "{{output}}"}))
        wf.add_connection("start", "weather_tool")
        wf.add_connection("weather_tool", "llm")
        wf.add_connection("llm", "end")

        result = await wf.invoke({"city": "Beijing"})
        assert result.state.value == "COMPLETED"
