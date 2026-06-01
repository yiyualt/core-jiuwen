LLM Examples
============

Configuration
-------------

.. code-block:: python

    from jiuwen.core.foundation.llm import ModelClientConfig, ModelRequestConfig

    # Connection settings
    client = ModelClientConfig(
        provider="openai",
        api_key="sk-...",
        api_base="https://api.openai.com/v1",
    )

    # Request parameters
    request = ModelRequestConfig(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1024,
    )

    print(request.model_dump())
    # {'model': 'gpt-4', 'temperature': 0.7, 'max_tokens': 1024, ...}

Using FakeLLMClient
-------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation.llm import FakeLLMClient, ModelRequestConfig


    async def main():
        client = FakeLLMClient([
            "The sky is blue because of Rayleigh scattering.",
            "Python was created by Guido van Rossum.",
        ])

        config = ModelRequestConfig(model="fake-model")

        # Chat
        answer = await client.chat(
            [{"role": "user", "content": "Why is the sky blue?"}],
            config=config,
        )
        print(answer)
        print(f"Calls made: {client.call_count}")  # 1

        # Chat stream
        async for token in client.chat_stream(
            [{"role": "user", "content": "Who created Python?"}],
        ):
            print(f"Token: {token}")

    asyncio.run(main())

Implementing a Real Provider
----------------------------

.. code-block:: python

    from typing import AsyncIterator
    from jiuwen.core.foundation.llm import LLMClient, ModelClientConfig, ModelRequestConfig


    class MyLLMClient(LLMClient):
        """Example: implement a real provider."""

        def __init__(self, config: ModelClientConfig):
            self.config = config

        async def chat(self, messages: list[dict], config: ModelRequestConfig | None = None) -> str:
            # TODO: call real API
            return "real response"

        async def chat_stream(self, messages: list[dict], config: ModelRequestConfig | None = None) -> AsyncIterator[str]:
            text = await self.chat(messages, config)
            for word in text.split():
                yield word + " "
