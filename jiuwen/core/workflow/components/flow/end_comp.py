# coding: utf-8
"""End component — the exit point of a workflow."""

import string
from typing import AsyncIterator

from pydantic import BaseModel, Field

from jiuwen.core.workflow.components.component import WorkflowComponent


class EndConfig(BaseModel):
    """Configuration for the End component.

    Attributes:
        response_template: Optional template string using {{variable}} syntax.
    """

    response_template: str = Field(
        default="",
        alias="responseTemplate",
        description="Response template for formatting final output",
    )
    model_config = {"populate_by_name": True}


class End(WorkflowComponent):
    """Exit point component. Collects inputs and produces final output.

    Usage::

        end = End()
        end = End({"responseTemplate": "The answer is: {{output}}"})
    """

    def __init__(self, conf: EndConfig | dict | None = None):
        super().__init__()
        if conf:
            try:
                self._conf = EndConfig.model_validate(conf)
            except Exception as e:
                raise ValueError(f"Invalid End component config: {e}") from e
        else:
            self._conf = None

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        if self._conf and self._conf.response_template:
            rendered = self._render(self._conf.response_template, inputs or {})
            return {"response": rendered}
        else:
            output = (
                {k: v for k, v in inputs.items() if v is not None}
                if isinstance(inputs, dict)
                else inputs
            )
            return {"output": output}

    async def stream(self, inputs: dict, **kwargs) -> AsyncIterator[dict]:
        if self._conf and self._conf.response_template:
            yield {"response": self._render(self._conf.response_template, inputs or {})}
        elif isinstance(inputs, dict):
            for key, value in inputs.items():
                yield {"output": {key: value}}
        else:
            yield {"output": inputs}

    @staticmethod
    def _render(template: str, inputs: dict) -> str:
        converted = template.replace("{{", "$").replace("}}", "")
        t = string.Template(converted)
        return t.safe_substitute(**inputs)
