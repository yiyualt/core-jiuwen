# coding: utf-8
"""ExperienceStore — file-backed, searchable optimization memory."""

import json
import os
import time
from pathlib import Path
from typing import Any


class ExperienceStore:
    """Persistent, searchable store of optimization experiences.

    Records successes and failures to a JSONL file. Future sessions
    can search past experiences and inject relevant ones as context.

    Usage::

        store = ExperienceStore("auto_harness_experiences.jsonl")
        store.record(ExperienceStore.SUCCESS, "optimize db", "Fixed N+1 queries")
        results = store.search("database performance", top_k=5)
        context = store.synthesize(results, max_tokens=2000)
    """

    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    INSIGHT = "INSIGHT"

    def __init__(self, file_path: str | None = None):
        self._file_path = file_path
        self._records: list[dict[str, Any]] = []
        if file_path:
            self._load()

    def record(self, stage: str, task: str, result: dict[str, Any],
               exp_type: str = SUCCESS) -> None:
        entry = {
            "type": exp_type,
            "stage": stage,
            "task": task[:300],
            "summary": str(result.get("result", ""))[:1000],
            "timestamp": time.time(),
        }
        self._records.append(entry)
        if self._file_path:
            self._append_to_file(entry)

    def record_failure(self, stage: str, task: str, error: str) -> None:
        self.record(stage, task, {"result": error}, exp_type=self.FAILURE)

    def record_insight(self, stage: str, topic: str, insight: str) -> None:
        self.record(stage, topic, {"result": insight}, exp_type=self.INSIGHT)

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """Keyword search with recency scoring.

        Args:
            query: Search terms (space-separated).
            top_k: Max results.

        Returns:
            Scored and sorted results.
        """
        terms = query.lower().split()
        now = time.time()
        scored = []
        for r in self._records:
            text = f"{r.get('task','')} {r.get('summary','')}".lower()
            score = sum(1 for t in terms if t in text)
            if score > 0:
                age_days = (now - r.get("timestamp", now)) / 86400
                recency = 1.0 if age_days < 1 else (0.5 if age_days < 7 else 0.2)
                scored.append((score * recency, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in scored[:top_k]]

    def synthesize(self, experiences: list[dict], max_tokens: int = 2000) -> str:
        """Generate a context string from experiences for agent injection."""
        if not experiences:
            return ""
        groups: dict[str, list] = {"SUCCESS": [], "FAILURE": [], "INSIGHT": []}
        for exp in experiences:
            groups.get(exp.get("type", "INSIGHT"), groups["INSIGHT"]).append(exp)

        parts = []
        total_chars = 0
        for label in ["SUCCESS", "FAILURE", "INSIGHT"]:
            items = groups[label]
            if not items:
                continue
            parts.append(f"## {label}")
            for item in items[:5]:
                line = f"- {item['task'][:100]}: {item['summary'][:200]}"
                total_chars += len(line)
                if total_chars > max_tokens * 4:
                    break
                parts.append(line)
        return "\n".join(parts)

    def recent(self, stage: str | None = None, limit: int = 10) -> list[dict]:
        records = self._records
        if stage:
            records = [r for r in records if r["stage"] == stage]
        return records[-limit:]

    def clear(self) -> None:
        self._records.clear()
        if self._file_path and os.path.exists(self._file_path):
            os.remove(self._file_path)

    def __len__(self) -> int:
        return len(self._records)

    def _load(self) -> None:
        path = self._file_path
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self._records.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

    def _append_to_file(self, entry: dict) -> None:
        if self._file_path:
            Path(self._file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self._file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
