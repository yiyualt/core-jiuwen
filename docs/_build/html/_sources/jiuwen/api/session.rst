``jiuwen.core.session``
========================

.. module:: jiuwen.core.session

Session
-------

.. class:: Session

   Conversation memory for multi-turn agents.

   .. method:: add_message(role: str, content: str) -> None
   .. method:: get_messages() -> list[dict]
   .. method:: clear() -> None
   .. method:: set_state(key: str, value) -> None
   .. method:: get_state(key: str, default=None) -> Any
   .. method:: __len__() -> int

StreamEmitter
-------------

.. class:: StreamEmitter

   Async stream for real-time agent output.

   .. method:: async emit(chunk) -> None
   .. method:: async close() -> None
   .. method:: async __aiter__() -> AsyncIterator
