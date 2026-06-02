# coding: utf-8
"""EventHandler — receives and processes task events."""

import sys
from abc import ABC


class EventHandler(ABC):
    """Abstract handler for task execution events.

    Subclass and override on_event() to add custom behavior
    (logging, metrics, notifications, etc.).
    """

    async def on_event(self, event) -> None:
        """Receive and process a task event.

        Args:
            event: TaskEvent instance.
        """
        ...


class LoggingHandler(EventHandler):
    """Default handler that logs events to stdout."""

    async def on_event(self, event) -> None:
        print(f"[{event.type}] {event.data}", file=sys.stderr, flush=True)
