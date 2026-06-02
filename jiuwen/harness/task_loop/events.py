# coding: utf-8
"""TaskEvent — execution event data class."""

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskEvent:
    """An event emitted during agent task execution.

    Attributes:
        type: Event type ("task_start", "tool_call", "task_complete", "error").
        data: Event payload dict.
        timestamp: Unix timestamp of when the event was created.
    """

    type: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
