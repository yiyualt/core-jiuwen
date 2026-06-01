# coding: utf-8
"""Session — conversation memory for agents.

A Session stores the message history for multi-turn conversations.
Agents use it to maintain context across multiple invocations.
"""

from typing import Any


class Session:
    """Stores conversation history for multi-turn agent interactions.

    Usage::

        session = Session()
        result1 = await agent.run({"query": "I'm Bob"}, session=session)
        result2 = await agent.run({"query": "What's my name?"}, session=session)
        # Agent remembers the name from the first interaction
    """

    def __init__(self):
        self._messages: list[dict[str, str]] = []
        self._state: dict[str, Any] = {}

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history.

        Args:
            role: Message role ("user", "assistant", "system", etc.).
            content: Message content.
        """
        self._messages.append({"role": role, "content": content})

    def get_messages(self) -> list[dict[str, str]]:
        """Return a copy of all messages in the conversation.

        Returns:
            List of message dicts with "role" and "content" keys.
        """
        return list(self._messages)

    def clear(self) -> None:
        """Reset the conversation history."""
        self._messages.clear()
        self._state.clear()

    def set_state(self, key: str, value: Any) -> None:
        """Store arbitrary state in the session."""
        self._state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Retrieve state from the session."""
        return self._state.get(key, default)

    def __len__(self) -> int:
        return len(self._messages)
