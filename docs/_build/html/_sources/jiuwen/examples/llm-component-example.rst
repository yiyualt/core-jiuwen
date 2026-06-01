LLM Component Examples
=======================

Setup: copy ``.env.example`` to ``.env`` and fill in your API key.

Basic LLM Component
-------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig


    async def main():
        config = LLMCompConfig(
            template_content=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "{{query}}"},
            ],
        )
        comp = LLMComponent(config)  # auto-detects OpenAIClient from .env

        result = await comp.invoke({"query": "What is Python?"})
        print(result["output"])

    asyncio.run(main())

LLM + Tool Pipeline
-------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import ToolCard, ToolComponent
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig


    def get_weather(city: str) -> str:
        return f"Sunny, 25C in {city}"


    async def main():
        tool_card = ToolCard(
            name="get_weather",
            description="Get current weather",
            parameters={"city": {"type": "string"}},
            func=get_weather,
        )

        llm_config = LLMCompConfig(
            template_content=[
                {"role": "user", "content": "Weather data: {{output}}. Summarize it."},
            ],
        )

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("weather", ToolComponent(tool_card))
        wf.add_workflow_comp("llm", LLMComponent(llm_config))
        wf.set_end_comp("end", End({"responseTemplate": "{{output}}"}))

        wf.add_connection("start", "weather")
        wf.add_connection("weather", "llm")
        wf.add_connection("llm", "end")

        result = await wf.invoke({"city": "Tokyo"})
        print(result.state)  # COMPLETED

    asyncio.run(main())

Full Workflow with Real LLM
----------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig


    async def main():
        client = OpenAIClient.from_env()

        config = LLMCompConfig(
            template_content=[
                {"role": "system", "content": "You are a poet."},
                {"role": "user", "content": "Write a short poem about: {{topic}}"},
            ],
        )

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("poet", LLMComponent(config, client))
        wf.set_end_comp("end", End({"responseTemplate": "{{output}}"}))

        wf.add_connection("start", "poet")
        wf.add_connection("poet", "end")

        result = await wf.invoke({"topic": "spring"})
        print(result.result)  # a real poem from GPT!

    asyncio.run(main())
