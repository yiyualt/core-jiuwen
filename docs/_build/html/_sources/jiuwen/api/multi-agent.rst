``jiuwen.core.multi_agent``
==============================

.. module:: jiuwen.core.multi_agent

MessageBus
----------

.. class:: MessageBus

   .. method:: subscribe(topic: str, handler) -> None
   .. method:: unsubscribe(topic: str, handler) -> None
   .. method:: async publish(topic: str, message: dict) -> None

TeamRuntime
-----------

.. class:: TeamRuntime(bus: MessageBus | None = None)

   .. method:: register(name: str, agent, capabilities: list[str] | None = None) -> None
   .. method:: unregister(name: str) -> None
   .. method:: route(task: str) -> str | None
   .. method:: async broadcast(topic: str, message: dict) -> None

handoff
-------

.. function:: async handoff(source_agent, target_agent, task: str, session=None) -> dict
