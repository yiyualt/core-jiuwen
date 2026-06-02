# coding: utf-8
"""QuestionerComponent — asks for missing input before proceeding."""

from jiuwen.core.workflow.components.component import WorkflowComponent


class QuestionerComponent(WorkflowComponent):
    """Asks the user for missing required fields.

    If the specified field is present in inputs, passes it through.
    Otherwise, returns a question asking the user to provide it.

    Usage::

        comp = QuestionerComponent("What is your name?", "name")
        result = await comp.invoke({})  # → {"question": "What is your name?", "field": "name"}
        result = await comp.invoke({"name": "Alice"})  # → {"output": "Alice"}
    """

    def __init__(self, question: str, field_name: str):
        super().__init__()
        self._question = question
        self._field_name = field_name

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        value = inputs.get(self._field_name)
        if value is not None and value != "":
            return {"output": value}
        return {"question": self._question, "field": self._field_name}
