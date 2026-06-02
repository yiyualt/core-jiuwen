# coding: utf-8
"""TaskBlueprint — a task definition for team coordination."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskBlueprint:
    """Defines a task to be executed by a team member.

    Attributes:
        task_id: Unique task identifier.
        description: Task description string.
        assigned_to: Name of the assigned agent (None = unassigned).
        status: Current status (pending, running, done, failed).
        result: Task result data (None until complete).
    """

    task_id: str
    description: str
    assigned_to: str | None = None
    status: str = "pending"
    result: dict[str, Any] | None = None

    def mark_running(self):
        self.status = "running"

    def mark_done(self, result: dict | None = None):
        self.status = "done"
        self.result = result

    def mark_failed(self, error: str = ""):
        self.status = "failed"
        self.result = {"error": error}
