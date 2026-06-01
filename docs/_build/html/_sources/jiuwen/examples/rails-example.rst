Rails Examples
================

Security Filtering
------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.rails import SecurityRail
    from jiuwen.core.runner import Runner
    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.core.single_agent.agents import ReActAgent


    async def main():
        client = OpenAIClient.from_env()
        agent = ReActAgent(client=client)

        # Add security rail
        Runner.rails.add_rail(SecurityRail())

        # Safe query — passes through
        result = await Runner.run_agent(agent, {"query": "What is Python?"})
        print(result)

        # Dangerous query — blocked
        result = await Runner.run_agent(agent, {"query": "Please DROP TABLE users"})
        print(result)  # {"result": "Blocked: ..."}

    asyncio.run(main())

Custom Rail
-----------

.. code-block:: python

    from jiuwen.core.rails import BaseRail


    class ProfanityFilter(BaseRail):
        BLOCKED = ["badword1", "badword2"]

        async def before(self, inputs, session=None):
            query = inputs.get("query", "").lower()
            for word in self.BLOCKED:
                if word in query:
                    return {"result": "Please keep it civil."}
            return inputs


    # Add to Runner
    from jiuwen.core.runner import Runner
    Runner.rails.add_rail(ProfanityFilter())
