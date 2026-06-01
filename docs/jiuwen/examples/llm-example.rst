LLM Examples
============

Setup
-----

Create a ``.env`` file (copy from ``.env.example``):

.. code-block:: bash

    cp .env.example .env
    # Edit .env with your API key

Basic Chat
----------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient, ModelRequestConfig


    async def main():
        client = OpenAIClient.from_env()

        response = await client.chat(
            [{"role": "user", "content": "What is the capital of France?"}],
        )
        print(response)

    asyncio.run(main())

Explicit Configuration
----------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import (
        OpenAIClient, ModelClientConfig, ModelRequestConfig,
    )


    async def main():
        client = OpenAIClient(ModelClientConfig(
            provider="openai",
            api_key="sk-your-key",
            api_base="https://api.openai.com/v1",
        ))

        config = ModelRequestConfig(model="gpt-4o", temperature=0.5, max_tokens=256)

        response = await client.chat(
            [{"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content": "Say hello in 3 languages."}],
            config,
        )
        print(response)

    asyncio.run(main())

Streaming
---------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient


    async def main():
        client = OpenAIClient.from_env()

        async for token in client.chat_stream(
            [{"role": "user", "content": "Write a haiku about coding."}],
        ):
            print(token, end="", flush=True)

    asyncio.run(main())
