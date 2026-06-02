# coding: utf-8
"""MessageBuffer — manages a token-capped message list."""

from jiuwen.core.context_engine.token_counter import TokenCounter


class MessageBuffer:
    """Manages a list of messages with automatic trimming at max_tokens.

    Always keeps system messages. Trims oldest non-system messages
    first when the total exceeds the limit.

    Usage::

        buffer = MessageBuffer(max_tokens=4096)
        buffer.add("system", "You are helpful.")
        buffer.add("user", "Hello!")
        buffer.add("assistant", "Hi there!")
        messages = buffer.get_messages()  # trimmed if needed
    """

    def __init__(self, max_tokens: int = 4096, counter: TokenCounter | None = None):
        self._max_tokens = max_tokens
        self._counter = counter or TokenCounter()
        self._messages: list[dict] = []

    def add(self, role: str, content: str) -> None:
        """Add a message to the buffer."""
        self._messages.append({"role": role, "content": content})

    def add_system(self, content: str) -> None:
        self.add("system", content)

    def add_user(self, content: str) -> None:
        self.add("user", content)

    def add_assistant(self, content: str) -> None:
        self.add("assistant", content)

    def get_messages(self) -> list[dict]:
        """Return messages, trimmed to fit within max_tokens."""
        if self._counter.count(self._messages) <= self._max_tokens:
            return list(self._messages)

        # Separate system messages (always kept)
        system_msgs = [m for m in self._messages if m["role"] == "system"]
        other_msgs = [m for m in self._messages if m["role"] != "system"]

        # Trim from the beginning of non-system messages
        while other_msgs:
            total = self._counter.count(system_msgs + other_msgs)
            if total <= self._max_tokens:
                break
            # Remove oldest pair (user + assistant)
            if len(other_msgs) >= 2:
                other_msgs = other_msgs[2:]
            else:
                other_msgs = other_msgs[1:]

        return system_msgs + other_msgs

    def clear(self) -> None:
        """Reset the buffer."""
        self._messages.clear()
