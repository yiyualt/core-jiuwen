# coding: utf-8
"""Start component — the entry point of a workflow."""

from jiuwen.core.workflow.components.component import WorkflowComponent


class Start(WorkflowComponent):
    """Entry point component. Passes inputs through unchanged."""

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        return inputs
