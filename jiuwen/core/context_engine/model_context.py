# coding: utf-8
"""ModelContext — high-level API for conversation context management."""

from jiuwen.core.context_engine.message_buffer import MessageBuffer


class ModelContext:
    """High-level API for building and managing LLM conversation context.

    Wraps MessageBuffer with convenient add_* methods.

    Usage::

        ctx = ModelContext(max_tokens=4096)
        ctx.add_system("You are a helpful assistant.")
        ctx.add_user("What is Python?")
        ctx.add_assistant("Python is a programming language.")
        ctx.add_user("Tell me more.")
        messages = ctx.get_messages()  # trimmed to 4096 tokens
    """

    def __init__(self, max_tokens: int = 4096):
        self._buffer = MessageBuffer(max_tokens=max_tokens)

    def add_system(self, content: str) -> None:
        self._buffer.add_system(content)

    def add_user(self, content: str) -> None:
        self._buffer.add_user(content)

    def add_assistant(self, content: str) -> None:
        self._buffer.add_assistant(content)

    def add_messages(self, messages: list[dict]) -> None:
        for msg in messages:
            self._buffer.add(msg.get("role", "user"), msg.get("content", ""))

    def get_messages(self) -> list[dict]:
        return self._buffer.get_messages()

    @property
    def buffer(self) -> MessageBuffer:
        return self._buffer
