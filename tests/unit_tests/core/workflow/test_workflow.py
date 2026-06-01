# coding: utf-8
"""Tests for Workflow construction and execution."""

import pytest
from jiuwen.core.graph.executable import Executable
from jiuwen.core.workflow.base import WorkflowCard, WorkflowExecutionState
from jiuwen.core.workflow.workflow import Workflow
from jiuwen.core.workflow.components import Start, End


class EchoNode(Executable[dict, dict]):
    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    async def on_invoke(self, inputs: dict, **kwargs) -> dict:
        v = inputs.get("value", inputs.get("query", ""))
        return {"output": f"{self.prefix}{v}"}


class TransformNode(Executable[dict, dict]):
    async def on_invoke(self, inputs: dict, **kwargs) -> dict:
        return {"output": inputs.get("output", "").upper()}


class TestWorkflowConstruction:
    def test_default(self):
        wf = Workflow()
        assert wf.card is not None
        assert wf.card.id

    def test_with_card(self):
        card = WorkflowCard(id="wf-1", name="Test")
        assert Workflow(card).card.id == "wf-1"

    def test_register_components(self):
        wf = Workflow()
        wf.set_start_comp("s", EchoNode())
        wf.add_workflow_comp("m", TransformNode())
        wf.set_end_comp("e", EchoNode())
        assert len(wf.get_components()) == 3

    def test_same_component_start_and_end(self):
        wf = Workflow()
        comp = EchoNode()
        wf.set_start_comp("main", comp)
        wf.set_end_comp("main", comp)
        assert len(wf.get_components()) == 1

    def test_add_connection(self):
        wf = Workflow()
        wf.set_start_comp("a", EchoNode()).set_end_comp("b", EchoNode())
        wf.add_connection("a", "b")

    def test_fluent(self):
        wf = (Workflow()
              .set_start_comp("entry", Start())
              .add_workflow_comp("mid", TransformNode())
              .set_end_comp("exit", End())
              .add_connection("entry", "mid")
              .add_connection("mid", "exit"))
        assert len(wf.get_components()) == 3

    def test_get_graph(self):
        from jiuwen.core.graph.graph import PregelGraph
        assert isinstance(Workflow().get_graph(), PregelGraph)


class TestWorkflowExecution:
    @pytest.mark.asyncio
    async def test_start_to_end(self):
        wf = Workflow()
        wf.set_start_comp("s", Start())
        wf.set_end_comp("e", End())
        wf.add_connection("s", "e")
        result = await wf.invoke({"msg": "hello"})
        assert result.state == WorkflowExecutionState.COMPLETED

    @pytest.mark.asyncio
    async def test_three_component_pipeline(self):
        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("upper", TransformNode())
        wf.set_end_comp("end", End())
        wf.add_connection("start", "upper")
        wf.add_connection("upper", "end")
        result = await wf.invoke({"output": "hello"})
        assert result.state == WorkflowExecutionState.COMPLETED

    @pytest.mark.asyncio
    async def test_error_handling(self):
        class Failing(Executable[dict, dict]):
            async def on_invoke(self, inputs: dict, **kwargs) -> dict:
                raise ValueError("fail")

        wf = Workflow()
        wf.set_start_comp("f", Failing())
        wf.set_end_comp("f", Failing())
        result = await wf.invoke({})
        assert result.state == WorkflowExecutionState.ERROR

    @pytest.mark.asyncio
    async def test_preserves_components(self):
        comp = EchoNode()
        wf = Workflow()
        wf.set_start_comp("main", comp)
        wf.set_end_comp("main", comp)
        await wf.invoke({"value": "test"})
        assert wf.get_components()["main"] is comp
