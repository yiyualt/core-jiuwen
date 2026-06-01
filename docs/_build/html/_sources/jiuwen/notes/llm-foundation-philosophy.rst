LLM Foundation: OpenAI Client and Configuration
================================================

The ``jiuwen.core.foundation`` module provides the **LLM abstraction layer**
that powers AI agents.

Two Kinds of Configuration
--------------------------

.. list-table::
   :header-rows: 1

   * - Concern
     - Model
     - Example
   * - **Connection**
     - ``ModelClientConfig``
     - provider, api_key, api_base, SSL
   * - **Request**
     - ``ModelRequestConfig``
     - model name, temperature, tokens

This separation lets you share connection settings across multiple models
while varying request parameters per call.

OpenAIClient
------------

``OpenAIClient`` implements ``LLMClient`` using the OpenAI SDK.
It works with any OpenAI-compatible API (Azure, local models via Ollama, etc.).

**From environment variables (recommended):**

Create a ``.env`` file:

.. code-block:: bash

    OPENAI_API_KEY=sk-your-key
    OPENAI_API_BASE=https://api.openai.com/v1
    OPENAI_MODEL=gpt-4o

Then use it:

.. code-block:: python

    from jiuwen.core.foundation import OpenAIClient, ModelRequestConfig

    client = OpenAIClient.from_env()

    response = await client.chat(
        [{"role": "user", "content": "Hello!"}],
        ModelRequestConfig(model="gpt-4o", temperature=0.7),
    )
    print(response)

**Explicit configuration:**

.. code-block:: python

    from jiuwen.core.foundation import OpenAIClient, ModelClientConfig

    client = OpenAIClient(ModelClientConfig(
        provider="openai",
        api_key="sk-...",
        api_base="https://api.openai.com/v1",
    ))

Streaming
---------

.. code-block:: python

    async for token in client.chat_stream(
        [{"role": "user", "content": "Tell me a story"}],
    ):
        print(token, end="", flush=True)
