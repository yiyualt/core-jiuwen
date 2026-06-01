# coding: utf-8
"""Component metadata and configuration types."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ComponentAbility(Enum):
    """Capabilities that a component can support.

    Each ability represents a different I/O pattern:
    - INVOKE: batch input → batch output
    - STREAM: batch input → streaming output
    - COLLECT: streaming input → batch output
    - TRANSFORM: streaming input → streaming output
    """

    INVOKE = ("invoke", "batch in, batch out")
    STREAM = ("stream", "batch in, stream out")
    COLLECT = ("collect", "stream in, batch out")
    TRANSFORM = ("transform", "stream in, stream out")

    def __init__(self, name: str, desc: str):
        self._name = name
        self._desc = desc

    @property
    def name(self) -> str:
        return self._name

    @property
    def desc(self) -> str:
        return self._desc


@dataclass
class WorkflowComponentMetadata:
    """Metadata describing a component instance in a workflow."""

    node_id: str
    node_type: str
    node_name: str


@dataclass
class ComponentConfig:
    """Runtime configuration for a workflow component."""

    metadata: Optional[WorkflowComponentMetadata] = field(default=None)
