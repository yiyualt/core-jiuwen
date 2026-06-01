# coding: utf-8
"""Shared test fixtures for jiuwen."""

import pytest


class FakeLLM:
    """A fake LLM client that returns preprogrammed responses.

    Used in tests to avoid real API calls. Configure with
    a list of responses that will be returned in order.
    """

    def __init__(self, responses: list[str] | None = None):
        self.responses = responses or ["default response"]
        self.call_count = 0
        self.last_messages: list[dict] = []

    async def invoke(self, messages: list[dict]) -> str:
        """Return the next preprogrammed response."""
        self.last_messages = messages
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response


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
    """Fixture providing a FakeLLM instance."""
    return FakeLLM()


@pytest.fixture
def recording_handler():
    """Fixture providing a RecordingHandler instance."""
    return RecordingHandler()
