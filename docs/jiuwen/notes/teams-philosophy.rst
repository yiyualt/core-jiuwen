Agent Teams: Multi-Agent Collaboration
=========================================

A **Team** bundles specialized agents under a **Coordinator** that
breaks complex tasks into subtasks and delegates each to the right expert.

Architecture
------------

.. code-block:: text

    User: "Research AI safety and write a report"

    Team
    ├── Coordinator (ReActAgent with delegate tool)
    │   ├── Thought: Need research
    │   ├── Action: delegate("researcher", "AI safety")
    │   ├── Observation: "AI safety concerns: ..."
    │   ├── Thought: Now write
    │   ├── Action: delegate("writer", "Write report about...")
    │   └── Final Answer: the report
    │
    └── Members
        ├── Researcher (ReActAgent with search tools)
        └── Writer (ReActAgent, no tools)

Usage
-----

.. code-block:: python

    from jiuwen.core.single_agent.agents import ReActAgent
    from jiuwen.core.agent_teams import Team
    from jiuwen.core.foundation import OpenAIClient, ToolCard

    client = OpenAIClient.from_env()

    # Create specialists
    researcher = ReActAgent(
        client, tools=[search_tool],
        system_prompt="You are a research specialist. Find facts.",
    )
    writer = ReActAgent(
        client,
        system_prompt="You are a technical writer. Write clearly.",
    )

    # Form a team
    team = Team(members={"researcher": researcher, "writer": writer})
    result = await team.run("Research renewable energy and write a summary")
    print(result["result"])

How It Works
------------

Coordinator inherits from ReActAgent with a built-in ``delegate`` tool.
It automatically:
1. Analyzes the task
2. Picks the right member for each subtask
3. Collects results
4. Synthesizes a final answer
