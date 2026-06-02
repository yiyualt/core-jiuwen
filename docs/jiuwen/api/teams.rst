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
