``jiuwen.core.context_engine``
================================

.. module:: jiuwen.core.context_engine

TokenCounter
------------

.. class:: TokenCounter(model: str = "gpt-4")

   .. method:: count(messages: list[dict]) -> int

MessageBuffer
-------------

.. class:: MessageBuffer(max_tokens: int = 4096, counter: TokenCounter | None = None)

   .. method:: add(role: str, content: str) -> None
   .. method:: add_system(content: str) -> None
   .. method:: add_user(content: str) -> None
   .. method:: add_assistant(content: str) -> None
   .. method:: get_messages() -> list[dict]
   .. method:: clear() -> None

ModelContext
------------

.. class:: ModelContext(max_tokens: int = 4096)

   .. method:: add_system(content: str) -> None
   .. method:: add_user(content: str) -> None
   .. method:: add_assistant(content: str) -> None
   .. method:: add_messages(messages: list[dict]) -> None
   .. method:: get_messages() -> list[dict]
