Tool Examples
=============

Basic Tool Component
--------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import ToolCard, ToolComponent


    def multiply(a: int, b: int) -> int:
        return a * b

    card = ToolCard(
        name="multiplier",
        description="Multiply two numbers",
        parameters={
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
            },
            "required": ["a", "b"],
        },
        func=multiply,
    )

    comp = ToolComponent(card)
    result = asyncio.run(comp.invoke({"a": 6, "b": 7}))
    print(result)  # {"output": 42}

Async Tool
----------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import ToolCard, ToolComponent


    async def fetch_data(url: str) -> str:
        # Simulate async API call
        await asyncio.sleep(0.01)
        return f"data from {url}"

    card = ToolCard(name="fetcher", func=fetch_data)
    comp = ToolComponent(card)
    result = asyncio.run(comp.invoke({"url": "https://api.example.com"}))
    print(result)  # {"output": "data from https://api.example.com"}

Tool in Workflow Pipeline
-------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.foundation import ToolCard, ToolComponent


    def calculate(x: int) -> int:
        return x * x + 2 * x + 1  # (x + 1)^2

    card = ToolCard(name="calc", func=calculate)

    wf = Workflow()
    wf.set_start_comp("start", Start())
    wf.add_workflow_comp("calc", ToolComponent(card))
    wf.set_end_comp("end", End({"responseTemplate": "Result: {{output}}"}))

    wf.add_connection("start", "calc")
    wf.add_connection("calc", "end")

    result = asyncio.run(wf.invoke({"x": 5}))
    print(result.state)  # COMPLETED

LLM + Tool Combined
-------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import (
        ToolCard, ToolComponent, FakeLLMClient,
        ModelClientConfig, ModelRequestConfig,
    )
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig


    def get_weather(city: str) -> str:
        return f"Sunny, 25C in {city}"

    tool_card = ToolCard(
        name="get_weather",
        description="Get current weather",
        parameters={"city": {"type": "string"}},
        func=get_weather,
    )

    llm_config = LLMCompConfig(
        template_content=[
            {"role": "user", "content": "The weather is {{output}}. Summarize briefly."},
        ],
    )
    llm_client = FakeLLMClient(["It's a beautiful sunny day!"])

    wf = Workflow()
    wf.set_start_comp("start", Start())
    wf.add_workflow_comp("weather", ToolComponent(tool_card))
    wf.add_workflow_comp("reporter", LLMComponent(llm_config, llm_client))
    wf.set_end_comp("end", End({"responseTemplate": "{{output}}"}))

    wf.add_connection("start", "weather")
    wf.add_connection("weather", "reporter")
    wf.add_connection("reporter", "end")

    result = asyncio.run(wf.invoke({"city": "Tokyo"}))
    print(result.state)  # COMPLETED
