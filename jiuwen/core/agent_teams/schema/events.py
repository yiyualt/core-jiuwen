# coding: utf-8
"""TeamEvent — structured event for team coordination."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TeamEvent:
    """An event emitted during team execution.

    Attributes:
        type: Event type (task_assigned, task_complete, agent_message, error).
        source: Name of the agent that emitted the event.
        target: Name of the target agent (if applicable).
        data: Event payload.
    """

    type: str
    source: str
    target: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
