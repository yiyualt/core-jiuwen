ReAct Agent Examples
=====================

Setup: configure ``.env`` with your OpenAI API key.

Basic ReAct Agent
-----------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient, ToolCard
    from jiuwen.core.single_agent.agents import ReActAgent


    def search(query: str) -> str:
        """Simulate a web search."""
        return f"Top result for '{query}': Python is a programming language."


    async def main():
        client = OpenAIClient.from_env()

        agent = ReActAgent(
            client=client,
            tools=[
                ToolCard(
                    name="search",
                    description="Search the web for information",
                    parameters={"properties": {"query": {"type": "string"}}},
                    func=search,
                ),
            ],
            system_prompt="You are a helpful research assistant.",
        )

        result = await agent.run({"query": "What is Python?"})
        print(result["result"])

    asyncio.run(main())

Multi-Tool Agent
-----------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient, ToolCard
    from jiuwen.core.single_agent.agents import ReActAgent


    def get_weather(city: str) -> str:
        return f"Weather in {city}: sunny, 22C"

    def calculate(expression: str) -> str:
        return str(eval(expression))


    async def main():
        client = OpenAIClient.from_env()

        agent = ReActAgent(
            client=client,
            tools=[
                ToolCard(name="get_weather", description="Get current weather for a city",
                         parameters={"properties": {"city": {"type": "string"}}},
                         func=get_weather),
                ToolCard(name="calculate", description="Evaluate a math expression",
                         parameters={"properties": {"expression": {"type": "string"}}},
                         func=calculate),
            ],
            system_prompt="You are a helpful assistant with access to weather and math tools.",
        )

        result = await agent.run({"query": "What's 15*7? And how's the weather in Tokyo?"})
        print(result["result"])

    asyncio.run(main())

Integration with Runner
------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.runner import Runner
    from jiuwen.core.foundation import OpenAIClient, ToolCard
    from jiuwen.core.single_agent.agents import ReActAgent


    async def main():
        client = OpenAIClient.from_env()
        agent = ReActAgent(client=client, tools=[...])

        result = await Runner.run_agent(agent, {"query": "Help me research AI."})
        print(result)

    asyncio.run(main())
