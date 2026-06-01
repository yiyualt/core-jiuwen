``jiuwen.core.rails``
======================

.. module:: jiuwen.core.rails

BaseRail
--------

.. class:: BaseRail

   Abstract base for agent middleware.

   .. method:: async before(inputs: dict, session=None) -> dict
   .. method:: async after(result: dict, session=None) -> dict

RailPipeline
------------

.. class:: RailPipeline(rails: list[BaseRail] | None = None)

   Orchestrates multiple rails. Execution: before → agent.run → after (reverse).

   .. method:: add_rail(rail: BaseRail) -> None
   .. property:: rails: list[BaseRail]
   .. method:: async run(agent, inputs, session=None) -> dict

SecurityRail
------------

.. class:: SecurityRail(blocked_terms: list[str] | None = None)

   Blocks dangerous content. Default blocked: rm, DROP TABLE, eval, etc.

   .. method:: async before(inputs: dict, session=None) -> dict
