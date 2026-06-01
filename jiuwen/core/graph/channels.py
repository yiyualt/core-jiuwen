# coding: utf-8
"""Channel system for graph message passing.

Channels mediate communication between graph nodes. Two types:
- TriggerChannel: fires when any message arrives (OR gate)
- BarrierChannel: fires only when ALL expected senders have arrived (AND gate)
"""

from abc import ABC, abstractmethod
from typing import Any, Set


class Channel(ABC):
    """Abstract base for message channels between graph nodes.

    Each channel belongs to a node and has a unique key for routing.
    """

    def __init__(self, node_name: str):
        self.name = node_name

    @property
    def key(self) -> str:
        """Unique routing key for this channel."""
        return f"channel:{self.name}"

    @property
    def node_name(self) -> str:
        """The node this channel feeds into."""
        return self.name

    @abstractmethod
    def is_ready(self) -> bool:
        """Whether the target node has enough messages to execute."""
        ...

    @abstractmethod
    def accept(self, message: Any) -> bool:
        """Accept a message. Returns True if state changed."""
        ...

    @abstractmethod
    def consume(self) -> None:
        """Consume messages, resetting readiness."""
        ...

    def snapshot(self) -> Any:
        """Return a serializable snapshot for state persistence."""
        return None

    def restore(self, state: Any) -> None:
        """Restore channel state from a snapshot."""
        pass


class TriggerChannel(Channel):
    """Fires when any message arrives. For simple pass-through edges."""

    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.messages: list = []

    def is_ready(self) -> bool:
        return len(self.messages) > 0

    def accept(self, message: Any) -> bool:
        self.messages.append(message)
        return True

    def consume(self) -> None:
        self.messages.clear()

    def snapshot(self) -> list:
        return list(self.messages)

    def restore(self, state: list) -> None:
        self.messages = list(state)


class BarrierChannel(Channel):
    """Fires only when ALL expected senders have sent a message.

    Used for nodes that need to wait for multiple upstream dependencies
    before executing (wait_for_all pattern).
    """

    def __init__(self, node_name: str, expected_senders: Set[str]):
        super().__init__(node_name)
        self.expected: Set[str] = expected_senders
        self.received: Set[str] = set()

    @property
    def key(self) -> str:
        senders = "|".join(sorted(self.expected))
        return f"barrier:{senders}->{self.name}"

    def is_ready(self) -> bool:
        return self.received == self.expected

    def accept(self, message: Any) -> bool:
        sender = getattr(message, "sender", None)
        if sender and sender in self.expected and sender not in self.received:
            self.received.add(sender)
            return True
        return False

    def consume(self) -> None:
        self.received.clear()

    def snapshot(self) -> list:
        return list(self.received)

    def restore(self, state: list) -> None:
        self.received = set(state)
