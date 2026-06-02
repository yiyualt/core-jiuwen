``jiuwen.core.agent_teams``
=============================

.. module:: jiuwen.core.agent_teams

Team
----

.. class:: Team(members: dict[str, Agent], client: LLMClient | None = None, system_prompt: str = "")

   A team of specialized agents coordinated by a leader.

   .. attribute:: members: dict

   .. method:: async run(task: str) -> dict

       Execute a complex task through the team.

CoordinatorAgent
----------------

.. class:: CoordinatorAgent(client, members=None, system_prompt="", max_iterations=10)

   ReActAgent with built-in delegation. Inherits from :class:`ReActAgent`.

InProcessMessager
-----------------

.. class:: InProcessMessager

   Async message passing between agents in the same process.

   .. method:: async send(target: str, message: dict) -> None
   .. method:: async receive(agent_name: str, timeout: float | None = None) -> dict

TeamEvent
---------

.. class:: TeamEvent(type: str, source: str, target: str | None = None, data: dict = {})

   Structured event for team coordination.

TaskBlueprint
-------------

.. class:: TaskBlueprint(task_id: str, description: str, assigned_to: str | None = None, status: str = "pending", result: dict | None = None)

   Task definition with lifecycle: mark_running(), mark_done(), mark_failed().

AgentSpawner
------------

.. class:: AgentSpawner(messager: InProcessMessager | None = None)

   Creates and manages child agents.

   .. method:: spawn(name: str, factory: Callable) -> Any
   .. method:: get(name: str) -> Any | None
   .. method:: remove(name: str) -> None
   .. attribute:: messager: InProcessMessager
   .. attribute:: agents: dict
