``jiuwen.core.runner``
========================

.. module:: jiuwen.core.runner

Runner
------

.. class:: Runner

   Global execution entry point.

   .. attribute:: resource_mgr: ResourceManager

       Process-global resource registry.

   .. classmethod:: async run_agent(agent, inputs: dict) -> dict

       Execute an agent with given inputs.

ResourceManager
---------------

.. class:: ResourceManager

   .. method:: add_workflow(key: str, factory: Callable) -> None
   .. method:: get_workflow(key: str) -> Workflow | None
   .. method:: add_tool(key: str, tool) -> None
   .. method:: get_tool(key: str) -> Any | None
