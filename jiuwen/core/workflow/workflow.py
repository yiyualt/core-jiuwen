# coding: utf-8
"""Workflow — the orchestrator for component DAG execution."""

import uuid
from typing import Self, Any

from jiuwen.core.graph.graph import PregelGraph
from jiuwen.core.workflow.base import (
    WorkflowCard,
    WorkflowExecutionState,
    WorkflowOutput,
)


class Workflow:
    """Orchestrates a directed graph of components.

    Components are connected via edges to form a processing pipeline.
    The workflow compiles and executes via the underlying PregelGraph.

    Usage::

        card = WorkflowCard(id="my_flow", name="My Workflow")
        flow = Workflow(card)
        flow.set_start_comp("start", start_component)
        flow.add_workflow_comp("llm", llm_component)
        flow.set_end_comp("end", end_component)
        flow.add_connection("start", "llm")
        flow.add_connection("llm", "end")
        result = await flow.invoke({"query": "Hello"})
    """

    def __init__(self, card: WorkflowCard | None = None):
        self._card = card if card else WorkflowCard(id=uuid.uuid4().hex)
        self._graph = PregelGraph()
        self._end_comp_id: str = ""
        self._components: dict[str, Any] = {}
        self._input_schemas: dict[str, Any] = {}

    @property
    def card(self) -> WorkflowCard:
        return self._card

    def set_start_comp(
        self, start_comp_id: str, component: Any, inputs_schema: dict | None = None
    ) -> Self:
        self._components.setdefault(start_comp_id, component)
        if start_comp_id not in self._graph.get_nodes():
            self._graph.add_node(start_comp_id, component)
        self._graph.start_node(start_comp_id)
        if inputs_schema:
            self._input_schemas[start_comp_id] = inputs_schema
        return self

    def add_workflow_comp(
        self, comp_id: str, component: Any, inputs_schema: dict | None = None
    ) -> Self:
        self._components[comp_id] = component
        self._graph.add_node(comp_id, component)
        if inputs_schema:
            self._input_schemas[comp_id] = inputs_schema
        return self

    def set_end_comp(
        self, end_comp_id: str, component: Any, inputs_schema: dict | None = None
    ) -> Self:
        self._end_comp_id = end_comp_id
        self._components.setdefault(end_comp_id, component)
        if end_comp_id not in self._graph.get_nodes():
            self._graph.add_node(end_comp_id, component)
        self._graph.end_node(end_comp_id)
        if inputs_schema:
            self._input_schemas[end_comp_id] = inputs_schema
        return self

    def add_connection(self, source_comp_id: str, target_comp_id: str) -> Self:
        self._graph.add_edge(source_comp_id, target_comp_id)
        return self

    def add_conditional_connection(self, source_comp_id: str, router: Any) -> Self:
        self._graph.add_conditional_edges(source_comp_id, router)
        return self

    async def invoke(self, inputs: dict[str, Any]) -> WorkflowOutput:
        compiled = self._graph.compile()
        try:
            result = await compiled._invoke(inputs)
            output = result.get(self._end_comp_id, result) if self._end_comp_id else result
            return WorkflowOutput(result=output, state=WorkflowExecutionState.COMPLETED)
        except Exception:
            return WorkflowOutput(result=None, state=WorkflowExecutionState.ERROR)

    def get_components(self) -> dict[str, Any]:
        return dict(self._components)

    def get_graph(self) -> PregelGraph:
        return self._graph
