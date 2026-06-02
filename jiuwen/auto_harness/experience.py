# coding: utf-8
"""ExperienceStore — accumulates and queries past optimization experiences."""

from typing import Any


class ExperienceStore:
    """Stores and retrieves optimization experiences.

    Records what worked and what didn't across pipeline runs,
    enabling future runs to learn from past results.

    Usage::

        store = ExperienceStore()
        store.record("assess", "fix bug", {"result": "found 3 issues"})
        recent = store.recent("assess", limit=5)
    """

    def __init__(self):
        self._records: list[dict[str, Any]] = []

    def record(self, stage: str, task: str, result: dict[str, Any]) -> None:
        """Record an optimization experience.

        Args:
            stage: Pipeline stage name.
            task: The task that was executed.
            result: The result of the execution.
        """
        self._records.append({
            "stage": stage,
            "task": task[:200],
            "result_summary": str(result.get("result", ""))[:500],
            "full_result": result,
        })

    def recent(self, stage: str | None = None, limit: int = 10) -> list[dict]:
        """Get recent experiences, optionally filtered by stage.

        Args:
            stage: Filter by stage name, or None for all.
            limit: Maximum number of records to return.

        Returns:
            List of recent experience records.
        """
        records = self._records
        if stage:
            records = [r for r in records if r["stage"] == stage]
        return records[-limit:]

    def clear(self) -> None:
        """Clear all stored experiences."""
        self._records.clear()

    def __len__(self) -> int:
        return len(self._records)
