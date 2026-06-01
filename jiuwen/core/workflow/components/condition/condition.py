# coding: utf-8
"""Condition — abstract condition evaluation for workflow branching.

Provides:
- Condition ABC: evaluate(state) → bool
- ExpressionCondition: evaluates a {{variable}} template expression
"""

import string
from abc import ABC, abstractmethod
from typing import Any


class Condition(ABC):
    """Abstract base for workflow conditions.

    Subclasses implement evaluate() to determine branch routing.
    """

    @abstractmethod
    def evaluate(self, state: dict[str, Any]) -> bool:
        """Evaluate the condition against the given state.

        Args:
            state: Current workflow state to evaluate against.

        Returns:
            True if the condition is met, False otherwise.
        """
        ...


class ExpressionCondition(Condition):
    """A condition that evaluates a template expression.

    Uses {{variable}} syntax for variable substitution, then
    evaluates the resulting expression as Python code.

    Usage::

        cond = ExpressionCondition("{{score}} > 60")
        cond.evaluate({"score": 85})  # True
        cond.evaluate({"score": 50})  # False

        cond = ExpressionCondition("{{status}} == 'active'")
        cond.evaluate({"status": "active"})  # True
    """

    def __init__(self, expression: str):
        """Initialize with a template expression.

        Args:
            expression: String with {{variable}} placeholders.
                       After substitution, must be valid Python boolean expression.
        """
        self._expression = expression

    def evaluate(self, state: dict[str, Any]) -> bool:
        """Render the template and evaluate as Python boolean expression.

        Args:
            state: Dict with values to substitute into the expression.

        Returns:
            Boolean result of the evaluated expression.
        """
        rendered = self._render(state)
        try:
            result = eval(rendered, {"__builtins__": {}}, {})
            return bool(result)
        except Exception:
            return False

    def _render(self, state: dict) -> str:
        """Replace {{var}} placeholders with values from state."""
        converted = self._expression.replace("{{", "$").replace("}}", "")
        t = string.Template(converted)

        # Convert all values to their repr for safe eval
        safe_state = {}
        for k, v in state.items():
            if isinstance(v, str):
                safe_state[k] = repr(v)
            else:
                safe_state[k] = str(v)
        return t.safe_substitute(**safe_state)
