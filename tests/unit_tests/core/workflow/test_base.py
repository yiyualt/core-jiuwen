# coding: utf-8
"""Tests for WorkflowCard, WorkflowExecutionState, WorkflowOutput, generate_workflow_key."""

from jiuwen.core.common import BaseCard
from jiuwen.core.workflow.base import (
    WorkflowCard,
    WorkflowExecutionState,
    WorkflowOutput,
    generate_workflow_key,
)


class TestWorkflowCard:
    def test_inherits_base_card(self):
        assert isinstance(WorkflowCard(), BaseCard)

    def test_defaults(self):
        card = WorkflowCard()
        assert card.version == ""
        assert card.input_params is None

    def test_full_construction(self):
        card = WorkflowCard(
            id="wf-1", name="text_gen", version="2.0",
            description="Generates text", input_params={"type": "object"},
        )
        assert card.id == "wf-1"
        assert card.version == "2.0"
        assert card.input_params == {"type": "object"}

    def test_tool_info(self):
        card = WorkflowCard(name="search", description="Search web", input_params={"q": {"type": "string"}})
        info = card.tool_info()
        assert info["name"] == "search"
        assert info["parameters"] == {"q": {"type": "string"}}

    def test_tool_info_none_params(self):
        assert WorkflowCard().tool_info()["parameters"] == {}


class TestWorkflowExecutionState:
    def test_values(self):
        assert WorkflowExecutionState.COMPLETED.value == "COMPLETED"
        assert WorkflowExecutionState.ERROR.value == "ERROR"
        assert WorkflowExecutionState.INPUT_REQUIRED.value == "INPUT_REQUIRED"


class TestWorkflowOutput:
    def test_success(self):
        out = WorkflowOutput(result={"key": "val"}, state=WorkflowExecutionState.COMPLETED)
        assert out.result == {"key": "val"}

    def test_serialization(self):
        out = WorkflowOutput(result={"x": 1}, state=WorkflowExecutionState.COMPLETED)
        d = out.model_dump()
        assert d["state"] == "COMPLETED"
        assert d["result"] == {"x": 1}


class TestGenerateWorkflowKey:
    def test_combines(self):
        assert generate_workflow_key("flow", "1.0") == "flow_1.0"
