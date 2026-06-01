LLM Component Examples
=======================

Basic LLM Pipeline
------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import FakeLLMClient, ModelClientConfig, ModelRequestConfig
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

    # Configure LLM with a fake client for testing
    config = LLMCompConfig(
        model_client_config=ModelClientConfig(provider="test"),
        model_config=ModelRequestConfig(model="test-model", temperature=0.7),
        template_content=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "{{query}}"},
        ],
    )
    client = FakeLLMClient(["The answer is 42."])

    # Build workflow
    wf = Workflow()
    wf.set_start_comp("start", Start())
    wf.add_workflow_comp("llm", LLMComponent(config, client))
    wf.set_end_comp("end", End({"responseTemplate": "LLM says: {{output}}"}))

    wf.add_connection("start", "llm")
    wf.add_connection("llm", "end")

    # Run
    result = asyncio.run(wf.invoke({"query": "What is the meaning of life?"}))
    print(result.state)  # COMPLETED

Custom Output Schema
--------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import FakeLLMClient, ModelClientConfig, ModelRequestConfig
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

    config = LLMCompConfig(
        model_client_config=ModelClientConfig(provider="openai"),
        model_config=ModelRequestConfig(model="gpt-4"),
        template_content=[
            {"role": "system", "content": "Extract entities from the text."},
            {"role": "user", "content": "{{text}}"},
        ],
        output_config={
            "type": "object",
            "properties": {
                "entities": {"type": "array", "items": {"type": "string"}},
            },
        },
    )

    client = FakeLLMClient(['{"entities": ["Apple", "Google"]}'])
    comp = LLMComponent(config, client)
    result = asyncio.run(comp.invoke({"text": "Apple and Google are tech companies."}))
    print(result["output"])

Streaming LLM Output
--------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import FakeLLMClient
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

    config = LLMCompConfig(
        template_content=[{"role": "user", "content": "{{query}}"}],
    )
    client = FakeLLMClient(["Streaming response"])

    async def main():
        comp = LLMComponent(config, client)
        async for chunk in comp.stream({"query": "Tell me a story"}):
            print(chunk["output"], end="")

    asyncio.run(main())
