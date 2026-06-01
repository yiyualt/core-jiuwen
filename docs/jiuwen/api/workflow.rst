``jiuwen.core.workflow``
==========================

.. module:: jiuwen.core.workflow

WorkflowCard
------------

.. class:: WorkflowCard

   Metadata card for workflows. Inherits from :class:`BaseCard`.

   .. attribute:: version: str
   .. attribute:: input_params: dict[str, Any] | None

   .. method:: tool_info() -> dict

WorkflowExecutionState
----------------------

.. class:: WorkflowExecutionState

   Enum: ``COMPLETED``, ``INPUT_REQUIRED``, ``ERROR``

WorkflowOutput
--------------

.. class:: WorkflowOutput

   .. attribute:: result: Any
   .. attribute:: state: WorkflowExecutionState

Workflow
--------

.. class:: Workflow(card: WorkflowCard | None = None)

   Orchestrates a graph of components.

   .. attribute:: card: WorkflowCard

   .. method:: set_start_comp(start_comp_id: str, component, inputs_schema=None) -> Self
   .. method:: add_workflow_comp(comp_id: str, component, inputs_schema=None) -> Self
   .. method:: set_end_comp(end_comp_id: str, component, inputs_schema=None) -> Self
   .. method:: add_connection(source_comp_id: str, target_comp_id: str) -> Self
   .. method:: add_conditional_connection(source_comp_id: str, router) -> Self
   .. method:: async invoke(inputs: dict[str, Any]) -> WorkflowOutput
   .. method:: get_components() -> dict[str, Any]
   .. method:: get_graph() -> PregelGraph

Functions
---------

.. function:: generate_workflow_key(workflow_id: str, workflow_version: str) -> str

   Return ``"{id}_{version}"``.
