# coding: utf-8
"""IntentDetectionComponent — keyword-based intent classification."""

from jiuwen.core.workflow.components.component import WorkflowComponent


class IntentDetectionComponent(WorkflowComponent):
    """Classifies user intent based on keyword matching.

    Usage::

        intents = {
            "greeting": ["hello", "hi", "hey"],
            "farewell": ["bye", "goodbye", "see you"],
            "help": ["help", "assist", "support"],
        }
        comp = IntentDetectionComponent(intents)
        result = await comp.invoke({"query": "hello there"})
        # → {"intent": "greeting", "confidence": 1.0}
    """

    def __init__(self, intents: dict[str, list[str]]):
        super().__init__()
        self._intents = intents

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        query = inputs.get("query", "").lower()
        for intent, keywords in self._intents.items():
            if any(kw.lower() in query for kw in keywords):
                return {"intent": intent, "confidence": 1.0}
        return {"intent": "unknown", "confidence": 0.0}
