# coding: utf-8
"""Tests for LLMComponent — LLM as a workflow component."""

import pytest
from jiuwen.core.foundation.llm import (
    ModelClientConfig,
    ModelRequestConfig,
    FakeLLMClient,
)
from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig


@pytest.fixture
def llm_config():
    return LLMCompConfig(
        model_client_config=ModelClientConfig(provider="test"),
        model_config=ModelRequestConfig(model="test-model"),
        template_content=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "{{query}}"},
        ],
    )


@pytest.fixture
def fake_client():
    return FakeLLMClient(["Hello! I'm here to help."])


class TestLLMCompConfig:
    def test_defaults(self):
        config = LLMCompConfig()
        assert config.template_content == []
        assert config.output_config is None

    def test_full(self):
        config = LLMCompConfig(
            model_client_config=ModelClientConfig(provider="openai"),
            model_config=ModelRequestConfig(model="gpt-4"),
            template_content=[{"role": "user", "content": "hi"}],
            output_config={"type": "object"},
        )
        assert config.output_config == {"type": "object"}


class TestLLMComponent:
    @pytest.mark.asyncio
    async def test_invoke_renders_template(self, llm_config):
        client = FakeLLMClient(["response"])
        comp = LLMComponent(llm_config, client)
        result = await comp.invoke({"query": "What is AI?"})
        assert client.last_messages[1]["content"] == "What is AI?"
        assert result["output"] == "response"

    @pytest.mark.asyncio
    async def test_invoke_with_default_client(self, llm_config):
        comp = LLMComponent(llm_config)
        result = await comp.invoke({"query": "test"})
        assert result["output"] == "default response"

    @pytest.mark.asyncio
    async def test_invoke_with_output_config(self, llm_config):
        llm_config.output_config = {"type": "object"}
        comp = LLMComponent(llm_config, FakeLLMClient(["structured"]))
        result = await comp.invoke({"query": "test"})
        assert result["output"] == "structured"
        assert result["response"] == "structured"

    @pytest.mark.asyncio
    async def test_stream(self, llm_config):
        comp = LLMComponent(llm_config, FakeLLMClient(["streamed"]))
        chunks = []
        async for chunk in comp.stream({"query": "test"}):
            chunks.append(chunk)
        assert chunks == [{"output": "streamed"}]

    @pytest.mark.asyncio
    async def test_multiple_template_variables(self, llm_config):
        llm_config.template_content = [
            {"role": "system", "content": "You are {{role}}."},
            {"role": "user", "content": "{{greeting}} {{name}}"},
        ]
        comp = LLMComponent(llm_config, FakeLLMClient(["ok"]))
        result = await comp.invoke({"role": "a poet", "greeting": "Hello", "name": "World"})
        assert result["output"] == "ok"

    def test_client_property(self, llm_config):
        client = FakeLLMClient()
        comp = LLMComponent(llm_config, client)
        assert comp.client is client


class TestLLMComponentIntegration:
    @pytest.mark.asyncio
    async def test_start_llm_end_pipeline(self):
        from jiuwen.core.workflow import Workflow, Start, End

        config = LLMCompConfig(
            model_client_config=ModelClientConfig(provider="test"),
            model_config=ModelRequestConfig(model="test"),
            template_content=[
                {"role": "user", "content": "{{query}}"},
            ],
        )
        client = FakeLLMClient(["The answer is 42."])

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("llm", LLMComponent(config, client))
        wf.set_end_comp("end", End({"responseTemplate": "LLM says: {{output}}"}))
        wf.add_connection("start", "llm")
        wf.add_connection("llm", "end")

        result = await wf.invoke({"query": "What is the meaning of life?"})
        assert result.state.value == "COMPLETED"
