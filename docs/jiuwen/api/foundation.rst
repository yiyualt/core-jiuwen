``jiuwen.core.foundation``
============================

.. module:: jiuwen.core.foundation

ModelClientConfig
-----------------

.. class:: ModelClientConfig

   Connection configuration for an LLM provider.

   .. attribute:: provider: str (default "")
   .. attribute:: api_key: str (default "")
   .. attribute:: api_base: str (default "")
   .. attribute:: verify_ssl: bool (default True)

ModelRequestConfig
------------------

.. class:: ModelRequestConfig

   Request parameters for an LLM call.

   .. attribute:: model: str (default "")
   .. attribute:: temperature: float (default 0.7, range 0.0-2.0)
   .. attribute:: max_tokens: int (default 1024, min 1)
   .. attribute:: top_p: float (default 1.0, range 0.0-1.0)
   .. attribute:: stop: list[str] | None (default None)

LLMClient
---------

.. class:: LLMClient

   Abstract base class for LLM providers.

   .. method:: async chat(messages: list[dict], config: ModelRequestConfig | None = None) -> str
   .. method:: async chat_stream(messages: list[dict], config: ModelRequestConfig | None = None) -> AsyncIterator[str]

FakeLLMClient
-------------

.. class:: FakeLLMClient(responses: list[str] | None = None)

   Test double with preprogrammed responses.

   .. attribute:: responses: list[str]
   .. attribute:: call_count: int
   .. attribute:: last_messages: list[dict]
