Agent Teams Examples
=====================

Setup: configure ``.env`` with your OpenAI API key.

Research + Writing Team
-----------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient, ToolCard
    from jiuwen.core.single_agent.agents import ReActAgent
    from jiuwen.core.agent_teams import Team


    def search(query: str) -> str:
        """Simulate web search."""
        return f"Top result for '{query}': AI is transforming industries."


    def calculate(expr: str) -> str:
        return str(eval(expr))


    async def main():
        client = OpenAIClient.from_env()

        researcher = ReActAgent(
            client=client,
            tools=[
                ToolCard(name="search", description="Search the web",
                         parameters={"properties": {"query": {"type": "string"}}},
                         func=search),
            ],
            system_prompt="You are a research specialist. Find facts and data.",
        )

        analyst = ReActAgent(
            client=client,
            tools=[
                ToolCard(name="calculate", description="Evaluate math",
                         parameters={"properties": {"expr": {"type": "string"}}},
                         func=calculate),
            ],
            system_prompt="You analyze data and draw conclusions.",
        )

        writer = ReActAgent(
            client=client,
            system_prompt="You write clear, concise reports from research data.",
        )

        team = Team(members={
            "researcher": researcher,
            "analyst": analyst,
            "writer": writer,
        })

        result = await team.run(
            "Research the impact of AI on healthcare, analyze the data, and write a summary."
        )
        print(result["result"])

    asyncio.run(main())

Direct Coordinator Usage
------------------------

.. code-block:: python

    from jiuwen.core.agent_teams.team import CoordinatorAgent
    from jiuwen.core.foundation import OpenAIClient, ToolCard
    from jiuwen.core.single_agent.agents import ReActAgent

    client = OpenAIClient.from_env()

    # Create member agents
    coder = ReActAgent(client, system_prompt="You write Python code.")
    reviewer = ReActAgent(client, system_prompt="You review code for bugs.")

    # Create coordinator directly
    coordinator = CoordinatorAgent(
        client=client,
        members={"coder": coder, "reviewer": reviewer},
        system_prompt="You manage a software development team.",
    )

    result = await coordinator.run({"query": "Write a function to sort a list and review it."})
