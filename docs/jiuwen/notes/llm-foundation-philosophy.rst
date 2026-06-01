LLM Foundation: Configuration and Client Abstraction
=====================================================

The `jiuwen.core.foundation` module provides the **LLM abstraction layer**
that the rest of the SDK builds upon.

Two Kinds of Configuration
--------------------------

jiuwen separates LLM configuration into two concerns:

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
while varying request parameters per call:

.. code-block:: python

    # Shared connection
    client_config = ModelClientConfig(
        provider="openai",
        api_key=os.environ["OPENAI_API_KEY"],
    )

    # Different requests
    creative = ModelRequestConfig(model="gpt-4", temperature=1.0, max_tokens=2048)
    precise  = ModelRequestConfig(model="gpt-4", temperature=0.1, max_tokens=512)

LLMClient Interface
-------------------

The ``LLMClient`` ABC defines two methods:

- ``chat(messages, config) -> str`` — send messages, get complete response
- ``chat_stream(messages, config) -> AsyncIterator[str]`` — stream tokens

Provider implementations (e.g., OpenAI, Anthropic) extend this class.
v0.0.4 provides only the interface and a fake for testing.

FakeLLMClient for Testing
-------------------------

Tests should never call real LLM APIs. ``FakeLLMClient`` returns
preprogrammed responses:

.. code-block:: python

    from jiuwen.core.foundation import FakeLLMClient

    client = FakeLLMClient(["Hello!", "How can I help?"])

    response = await client.chat([{"role": "user", "content": "Hi"}])
    assert response == "Hello!"
    assert client.call_count == 1

    response = await client.chat([...])
    assert response == "How can I help?"

    # Wraps around after exhausting the list
    response = await client.chat([...])
    assert response == "Hello!"  # back to first
