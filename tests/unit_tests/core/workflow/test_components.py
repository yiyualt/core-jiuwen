# coding: utf-8
"""Tests for workflow components: WorkflowComponent, Start, End."""

import pytest
from jiuwen.core.workflow.components.component import WorkflowComponent
from jiuwen.core.workflow.components.base import ComponentAbility, ComponentConfig, WorkflowComponentMetadata
from jiuwen.core.workflow.components.flow.start_comp import Start
from jiuwen.core.workflow.components.flow.end_comp import End, EndConfig


class TestComponentAbility:
    def test_invoke(self):
        assert ComponentAbility.INVOKE.name == "invoke"

    def test_stream(self):
        assert ComponentAbility.STREAM.name == "stream"


class TestComponentConfig:
    def test_metadata(self):
        meta = WorkflowComponentMetadata(node_id="n1", node_type="LLM", node_name="chat")
        assert meta.node_type == "LLM"

    def test_config(self):
        meta = WorkflowComponentMetadata(node_id="n1", node_type="Start", node_name="entry")
        config = ComponentConfig(metadata=meta)
        assert config.metadata.node_type == "Start"


class TestCustomComponent:
    @pytest.mark.asyncio
    async def test_invoke(self):
        class Upper(WorkflowComponent):
            async def invoke(self, inputs: dict, **kwargs) -> dict:
                return {"result": inputs["text"].upper()}

        result = await Upper().invoke({"text": "hello"})
        assert result == {"result": "HELLO"}

    @pytest.mark.asyncio
    async def test_stream(self):
        class Splitter(WorkflowComponent):
            async def stream(self, inputs: dict, **kwargs):
                for w in inputs["text"].split():
                    yield {"word": w}

        results = []
        async for chunk in Splitter().stream({"text": "a b c"}):
            results.append(chunk)
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_unimplemented_raises(self):
        class Empty(WorkflowComponent):
            pass
        with pytest.raises(NotImplementedError):
            await Empty().invoke({})


class TestStartComponent:
    @pytest.mark.asyncio
    async def test_passthrough(self):
        result = await Start().invoke({"q": "hello", "n": 5})
        assert result == {"q": "hello", "n": 5}

    @pytest.mark.asyncio
    async def test_empty(self):
        assert await Start().invoke({}) == {}


class TestEndComponent:
    @pytest.mark.asyncio
    async def test_no_template(self):
        result = await End().invoke({"text": "hello"})
        assert result == {"output": {"text": "hello"}}

    @pytest.mark.asyncio
    async def test_filters_none(self):
        result = await End().invoke({"a": "v", "b": None})
        assert result["output"] == {"a": "v"}

    @pytest.mark.asyncio
    async def test_with_template(self):
        end = End({"responseTemplate": "Result: {{output}}"})
        result = await end.invoke({"output": "hello"})
        assert result == {"response": "Result: hello"}

    @pytest.mark.asyncio
    async def test_template_missing_var(self):
        end = End({"responseTemplate": "Hello {{name}}"})
        result = await end.invoke({})
        assert result["response"] == "Hello $name"

    @pytest.mark.asyncio
    async def test_stream_no_template(self):
        results = []
        async for chunk in End().stream({"a": "1", "b": "2"}):
            results.append(chunk)
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_stream_with_template(self):
        end = End({"responseTemplate": "Got: {{data}}"})
        results = [chunk async for chunk in end.stream({"data": "test"})]
        assert results == [{"response": "Got: test"}]

    @pytest.mark.asyncio
    async def test_extra_fields_ignored(self):
        # Pydantic v2 ignores extra fields — no error
        end = End({"responseTemplate": "ok: {{x}}", "extra": "ignored"})
        result = await end.invoke({"x": "val"})
        assert result == {"response": "ok: val"}
