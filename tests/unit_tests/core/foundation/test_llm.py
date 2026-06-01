# coding: utf-8
"""Tests for LLM client abstraction: configs, LLMClient ABC, FakeLLMClient."""

import pytest
from jiuwen.core.foundation.llm import (
    ModelClientConfig,
    ModelRequestConfig,
    LLMClient,
)
from tests.conftest import FakeLLMClient


class TestModelClientConfig:
    def test_defaults(self):
        c = ModelClientConfig()
        assert c.provider == ""
        assert c.api_key == ""
        assert c.api_base == ""
        assert c.verify_ssl is True

    def test_full(self):
        c = ModelClientConfig(provider="openai", api_key="sk-abc", api_base="https://api.openai.com", verify_ssl=False)
        assert c.provider == "openai"
        assert c.verify_ssl is False

    def test_serialize(self):
        c = ModelClientConfig(provider="test")
        d = c.model_dump()
        assert d["provider"] == "test"


class TestModelRequestConfig:
    def test_defaults(self):
        c = ModelRequestConfig(model="gpt-4")
        assert c.model == "gpt-4"
        assert c.temperature == 0.7
        assert c.max_tokens == 1024
        assert c.top_p == 1.0
        assert c.stop is None

    def test_temperature_bounds(self):
        with pytest.raises(Exception):
            ModelRequestConfig(model="x", temperature=3.0)


class TestLLMClient:
    def test_is_abstract(self):
        with pytest.raises(TypeError):
            LLMClient()


class TestFakeLLMClient:
    @pytest.mark.asyncio
    async def test_returns_configured_response(self):
        client = FakeLLMClient(["hello"])
        result = await client.chat([{"role": "user", "content": "hi"}])
        assert result == "hello"

    @pytest.mark.asyncio
    async def test_default_response(self):
        client = FakeLLMClient()
        result = await client.chat([])
        assert result == "default response"

    @pytest.mark.asyncio
    async def test_cycles_responses(self):
        client = FakeLLMClient(["a", "b"])
        assert await client.chat([]) == "a"
        assert await client.chat([]) == "b"
        assert await client.chat([]) == "a"

    @pytest.mark.asyncio
    async def test_tracks_call_count(self):
        client = FakeLLMClient(["x", "y", "z"])
        await client.chat([])
        await client.chat([])
        assert client.call_count == 2

    @pytest.mark.asyncio
    async def test_records_last_messages(self):
        client = FakeLLMClient(["ok"])
        msgs = [{"role": "user", "content": "hi"}]
        await client.chat(msgs)
        assert client.last_messages == msgs

    @pytest.mark.asyncio
    async def test_chat_stream_yields_response(self):
        client = FakeLLMClient(["streamed"])
        chunks = []
        async for chunk in client.chat_stream([{"role": "user", "content": "hey"}]):
            chunks.append(chunk)
        assert chunks == ["streamed"]
        assert client.call_count == 1

    @pytest.mark.asyncio
    async def test_accepts_config_parameter(self):
        client = FakeLLMClient(["ok"])
        config = ModelRequestConfig(model="test-model", temperature=0.5)
        result = await client.chat([], config=config)
        assert result == "ok"


class TestConftestFixture:
    def test_fake_llm_returns_fake_llm_client(self, fake_llm):
        assert isinstance(fake_llm, FakeLLMClient)

    @pytest.mark.asyncio
    async def test_fake_llm_works(self, fake_llm):
        result = await fake_llm.chat([{"role": "user", "content": "test"}])
        assert result == "default response"

    def test_recording_handler(self, recording_handler):
        recording_handler({"event": "test"})
        assert recording_handler.event_count == 1
