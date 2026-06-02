# coding: utf-8
"""MessageBus — publish-subscribe messaging for multi-agent systems."""

import asyncio
from collections import defaultdict
from typing import Any, Callable, Awaitable

Handler = Callable[[dict[str, Any]], Awaitable[None]]


class MessageBus:
    """Central pub-sub message bus for agents.

    Agents subscribe to topics and publish messages. All handlers
    for a topic are called concurrently when a message arrives.

    Usage::

        bus = MessageBus()

        async def handler(msg):
            print(f"Got: {msg}")

        bus.subscribe("tasks", handler)
        await bus.publish("tasks", {"task": "search", "query": "AI"})
    """

    def __init__(self):
        self._subscribers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Handler) -> None:
        """Subscribe a handler to a topic.

        Args:
            topic: Topic name to subscribe to.
            handler: Async callable that receives message dicts.
        """
        self._subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Handler) -> None:
        """Remove a handler from a topic."""
        handlers = self._subscribers.get(topic, [])
        if handler in handlers:
            handlers.remove(handler)

    async def publish(self, topic: str, message: dict[str, Any]) -> None:
        """Publish a message to all subscribers of a topic.

        Args:
            topic: Topic to publish to.
            message: Message dict to deliver.
        """
        handlers = self._subscribers.get(topic, [])
        if not handlers:
            return
        tasks = [handler(message) for handler in handlers]
        await asyncio.gather(*tasks)
