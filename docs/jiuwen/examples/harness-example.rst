Harness Examples
================

Setup: configure ``.env`` with your OpenAI API key.

Basic Coding Agent
------------------

.. code-block:: python

    import asyncio
    from jiuwen.harness import create_deep_agent


    async def main():
        agent = create_deep_agent(workspace_dir="./my-project")

        result = await agent.run({
            "query": "Create a file called hello.py that prints 'Hello, World!'"
        })
        print(result["result"])

    asyncio.run(main())

Custom Configuration
--------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.harness import DeepAgent, DeepAgentConfig


    async def main():
        client = OpenAIClient.from_env()
        agent = DeepAgent(client, DeepAgentConfig(
            workspace_dir="/path/to/project",
            system_prompt="You are a Python expert. Write clean, tested code.",
            max_iterations=30,
        ))

        result = await agent.run({
            "query": "Refactor the database module to use async/await."
        })
        print(result["result"])

    asyncio.run(main())

Using Workspace Directly
------------------------

.. code-block:: python

    from jiuwen.harness import Workspace

    ws = Workspace("/tmp/my-project")
    ws.write_file("README.md", "# My Project\\n\\nHello!")
    print(ws.list_files())
    print(ws.read_file("README.md"))
