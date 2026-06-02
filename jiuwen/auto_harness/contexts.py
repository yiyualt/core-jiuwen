# coding: utf-8
"""SessionContext — shared state carried through pipeline execution."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionContext:
    """Carries shared state across pipeline stages.

    Stages read from and write to this context to pass information
    between each other without direct coupling.
    """

    orchestrator: Any = None
    artifacts: dict[str, Any] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)

    def put_artifact(self, key: str, value: Any) -> None:
        """Store an artifact for use by later stages."""
        self.artifacts[key] = value

    def get_artifact(self, key: str, default: Any = None) -> Any:
        """Retrieve an artifact stored by a previous stage."""
        return self.artifacts.get(key, default)

    def add_message(self, msg: str) -> None:
        self.messages.append(msg)

    def clone(self) -> "SessionContext":
        """Create a shallow copy for fix-loop retries."""
        return SessionContext(
            orchestrator=self.orchestrator,
            artifacts=dict(self.artifacts),
            messages=list(self.messages),
        )
