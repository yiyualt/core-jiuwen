``jiuwen.core.single_agent``
==============================

.. module:: jiuwen.core.single_agent

AgentCard
---------

.. class:: AgentCard

   Metadata card for agents. Inherits from :class:`BaseCard`.

   .. attribute:: version: str (default "")
   .. attribute:: model: str (default "")

WorkflowAgentConfig
-------------------

.. class:: WorkflowAgentConfig

   .. attribute:: id: str (default "")
   .. attribute:: version: str (default "0.1.0")
   .. attribute:: description: str (default "")

WorkflowAgent
-------------

.. class:: WorkflowAgent(config: WorkflowAgentConfig)

   Agent that executes workflows.

   .. attribute:: config: WorkflowAgentConfig

   .. method:: add_workflows(workflows: list[Workflow]) -> None
   .. method:: async run(inputs: dict) -> dict

ReActAgent
----------

.. class:: ReActAgent(client: LLMClient, tools: list[ToolCard] | None = None, system_prompt: str = "", max_iterations: int = 10)

   Agent using the Reasoning + Acting paradigm.

   .. method:: async run(inputs: dict) -> dict

       Execute the ReAct loop. Inputs must contain ``"query"`` key.
