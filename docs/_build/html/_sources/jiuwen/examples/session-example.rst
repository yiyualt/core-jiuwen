Session Examples
================

Multi-Turn Conversation
-----------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.session import Session
    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.core.single_agent.agents import ReActAgent


    async def main():
        client = OpenAIClient.from_env()
        agent = ReActAgent(client=client)
        session = Session()

        # First turn
        result1 = await agent.run({"query": "My name is Alice."}, session=session)
        print(result1["result"])

        # Second turn — agent remembers
        result2 = await agent.run({"query": "What's my name?"}, session=session)
        print(result2["result"])  # "Your name is Alice."

        print(f"Messages in session: {len(session)}")

    asyncio.run(main())

Streaming with Session
----------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.session import Session
    from jiuwen.core.foundation import OpenAIClient, ToolCard
    from jiuwen.core.single_agent.agents import ReActAgent


    def search(query: str) -> str:
        return f"Results for: {query}"


    async def main():
        client = OpenAIClient.from_env()
        agent = ReActAgent(
            client=client,
            tools=[ToolCard(name="search", func=search, ...)],
        )
        session = Session()

        async for chunk in agent.stream(
            {"query": "Search for Python and summarize."},
            session=session,
        ):
            print(f"[{chunk['type']}] {chunk['data']}")

    asyncio.run(main())
