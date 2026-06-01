# coding: utf-8
"""Shared test fixtures for jiuwen.

Provides FakeLLMClient — a test double that returns preprogrammed responses.
This is the ONLY place FakeLLMClient exists; production code uses OpenAIClient.
"""

from typing import AsyncIterator

import pytest

from jiuwen.core.foundation.llm import LLMClient, ModelRequestConfig


class FakeLLMClient(LLMClient):
    """A fake LLM client that returns preprogrammed responses.

    Used in tests to avoid real API calls. Responses are returned
    in order, cycling when exhausted.

    Usage::

        client = FakeLLMClient(["Hello!", "How can I help?"])
        response = await client.chat([{"role": "user", "content": "Hi"}])
        assert response == "Hello!"
    """

    def __init__(self, responses: list[str] | None = None):
        self.responses: list[str] = responses or ["default response"]
        self.call_count: int = 0
        self.last_messages: list[dict] = []

    async def chat(self, messages: list[dict], config: ModelRequestConfig | None = None) -> str:
        """Return the next preprogrammed response."""
        self.last_messages = messages
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response

    async def chat_stream(self, messages: list[dict], config: ModelRequestConfig | None = None) -> AsyncIterator[str]:
        """Stream the preprogrammed response as a single chunk."""
        text = await self.chat(messages, config)
        yield text


class RecordingHandler:
    """A callback handler that records events for test verification."""

    def __init__(self):
        self.events: list[dict] = []

    def __call__(self, event: dict) -> None:
        self.events.append(event)

    @property
    def event_count(self) -> int:
        return len(self.events)


@pytest.fixture
def fake_llm():
    """Fixture providing a FakeLLMClient instance."""
    return FakeLLMClient()


@pytest.fixture
def recording_handler():
    """Fixture providing a RecordingHandler instance."""
    return RecordingHandler()
