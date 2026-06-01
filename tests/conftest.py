# coding: utf-8
"""Shared test fixtures for jiuwen."""

import pytest
from jiuwen.core.foundation.llm import FakeLLMClient


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
