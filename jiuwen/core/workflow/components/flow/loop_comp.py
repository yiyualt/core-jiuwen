# coding: utf-8
"""LoopComponent — repeats execution multiple times, accumulating results."""

from jiuwen.core.workflow.components.component import WorkflowComponent


class LoopComponent(WorkflowComponent):
    """Repeats execution up to max_iterations, collecting results.

    Each invocation adds the input item to a list. When max_iterations
    is reached, returns the full collection with done=True.

    Usage::

        comp = LoopComponent(max_iterations=3)
        r1 = await comp.invoke({"item": "a"})  # → {"items": ["a"], "count": 1, "done": False}
        r2 = await comp.invoke({"item": "b"})  # → {"items": ["a","b"], "count": 2, "done": False}
        r3 = await comp.invoke({"item": "c"})  # → {"items": ["a","b","c"], "count": 3, "done": True}
    """

    def __init__(self, max_iterations: int = 10):
        super().__init__()
        self._max_iterations = max_iterations
        self._items: list = []
        self._count: int = 0

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        item = inputs.get("item")
        if item is not None:
            self._items.append(item)
        self._count += 1
        done = self._count >= self._max_iterations
        return {"items": list(self._items), "count": self._count, "done": done}

    def reset(self) -> None:
        """Reset the loop counter and accumulated items."""
        self._items.clear()
        self._count = 0
