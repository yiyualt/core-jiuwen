# coding: utf-8
"""Case — a test case for evaluating agent performance."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Case:
    """A single test case: input → expected output.

    Usage::

        case = Case(input={"query": "What is 2+2?"}, expected="4")
    """

    input: dict[str, Any]
    expected: str
    metadata: dict[str, Any] = field(default_factory=dict)
