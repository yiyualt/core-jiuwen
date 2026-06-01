# coding: utf-8
"""Tool system — callable functions as workflow components.

Provides:
- ToolCard: metadata describing a tool (name, parameters, function)
- ToolComponent: wraps a ToolCard into a WorkflowComponent
"""

import inspect
from typing import Any, Callable

from pydantic import Field

from jiuwen.core.common import BaseCard
from jiuwen.core.workflow.components.component import WorkflowComponent


class ToolCard(BaseCard):
    """Metadata card for a callable tool.

    Extends BaseCard with a parameter schema and the actual function.

    Attributes:
        parameters: JSON Schema describing the tool's input parameters.
        func: The callable function. Excluded from serialization.
    """

    parameters: dict | None = None
    func: Callable[..., Any] | None = Field(default=None, exclude=True)

    def tool_info(self) -> dict:
        """Return structured metadata for tool-calling systems."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters or {},
        }


class ToolComponent(WorkflowComponent):
    """A workflow component that wraps a ToolCard.

    At invoke time, the component calls the tool's function with the
    provided inputs and returns the result.

    Usage::

        def add(a: int, b: int) -> int:
            return a + b

        card = ToolCard(name="adder", description="Add two numbers", func=add)
        comp = ToolComponent(card)
        result = await comp.invoke({"a": 3, "b": 4})
        # result = {"output": 7}
    """

    def __init__(self, card: ToolCard):
        super().__init__()
        self._card = card

    @property
    def card(self) -> ToolCard:
        return self._card

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        """Call the tool's function with the given inputs.

        Args:
            inputs: Keyword arguments passed to the tool function.

        Returns:
            Dict with "output" key containing the function's return value.

        Raises:
            ValueError: If the card has no function assigned.
        """
        if self._card.func is None:
            raise ValueError(f"Tool '{self._card.name}' has no function assigned")

        result = self._card.func(**inputs)
        if inspect.isawaitable(result):
            result = await result
        return {"output": result}
