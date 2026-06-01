# coding: utf-8
"""Workflow base types — metadata cards, execution state, and output containers."""

from enum import Enum
from typing import Any

from pydantic import BaseModel

from jiuwen.core.common import BaseCard


class WorkflowCard(BaseCard):
    """Metadata card for a workflow.

    Attributes:
        version: Workflow version string.
        input_params: JSON Schema describing expected input parameters.
    """

    version: str = ""
    input_params: dict[str, Any] | None = None

    def tool_info(self) -> dict:
        """Return tool-compatible metadata for this workflow."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.input_params if self.input_params else {},
        }


class WorkflowExecutionState(str, Enum):
    """Possible states of workflow execution."""

    COMPLETED = "COMPLETED"
    INPUT_REQUIRED = "INPUT_REQUIRED"
    ERROR = "ERROR"


class WorkflowOutput(BaseModel):
    """Final output container for workflow execution.

    Attributes:
        result: Output data from the workflow.
        state: Final state of the workflow execution.
    """

    result: Any
    state: WorkflowExecutionState


def generate_workflow_key(workflow_id: str, workflow_version: str) -> str:
    """Generate a unique key by combining ID and version."""
    return f"{workflow_id}_{workflow_version}"
