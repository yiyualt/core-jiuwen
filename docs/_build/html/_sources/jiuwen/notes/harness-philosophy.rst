Harness: Coding Agent Framework
================================

The **Harness** is the coding agent framework built on jiuwen core
primitives. It provides a ready-to-use agent for software engineering
tasks.

DeepAgent
---------

``DeepAgent`` extends ``ReActAgent`` with three coding tools:

- **bash**: Run shell commands and get output
- **read**: Read file contents
- **write**: Write content to files

.. code-block:: python

    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.harness import DeepAgent, DeepAgentConfig

    client = OpenAIClient.from_env()
    agent = DeepAgent(client, DeepAgentConfig(
        workspace_dir="/path/to/project",
    ))

    result = await agent.run({"query": "Find and fix the bug in main.py"})

Workspace
---------

``Workspace`` manages a project directory with safe sandboxing.
All paths are relative to the workspace root — attempts to escape
are blocked.

.. code-block:: python

    from jiuwen.harness import Workspace

    ws = Workspace("/path/to/project")
    ws.write_file("src/main.py", "print('hello')")
    content = ws.read_file("src/main.py")
    files = ws.list_files("*.py")

Factory
-------

For zero-config usage:

.. code-block:: python

    from jiuwen.harness import create_deep_agent

    # Auto-configure from .env
    agent = create_deep_agent()

    # Custom workspace
    agent = create_deep_agent(workspace_dir="./my-project")
