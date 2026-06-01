# coding: utf-8
"""Base classes for the jiuwen agent SDK.

Defines the foundational Card/Config split pattern:
- Cards are static metadata — serializable, transportable identity descriptors.
- Configs are runtime objects — hold resources, state, and behavior.
"""

import uuid

from pydantic import BaseModel, Field


class BaseCard(BaseModel):
    """Base class for all metadata cards.

    Cards describe identity and metadata for agents, tools, workflows, etc.
    They are serializable and can cross process boundaries.

    Attributes:
        id: Unique identifier, auto-generated UUID hex string.
        name: Human-readable name, unique within a namespace.
        description: Description of purpose, capabilities, and use cases.
    """

    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    name: str = Field(default="")
    description: str = Field(default="")

    def tool_info(self):
        """Return tool-compatible metadata for this card.

        Override in subclasses to provide structured tool descriptions.
        """
        ...

    def to_str(self) -> str:
        """Return a compact string representation."""
        return f"id={self.id},name={self.name}"
