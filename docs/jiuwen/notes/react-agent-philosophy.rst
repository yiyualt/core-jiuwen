ReAct Agent: Reasoning + Acting
================================

``ReActAgent`` implements the ReAct (Reasoning + Acting) paradigm.
Unlike ``WorkflowAgent`` (static pipeline), ReActAgent **dynamically**
decides which tools to call based on the user's question.

How It Works
------------

.. code-block:: text

    User: "What's the weather in Paris?"

    ┌──────────────────────────────────────┐
    │  ReAct Loop                           │
    │                                       │
    │  Thought: I need to check weather     │
    │  Action: get_weather(city='Paris')    │
    │       │                               │
    │       ▼                               │
    │  Observation: "Sunny, 22C"            │
    │       │                               │
    │       ▼                               │
    │  Thought: I have the data             │
    │  Final Answer: "It is sunny in Paris" │
    │                                       │
    └──────────────────────────────────────┘

The agent automatically:
1. Analyzes the question
2. Chooses appropriate tools
3. Executes them
4. Interprets results
5. Produces a final answer

Tool Discovery
--------------

Tools are automatically described in the system prompt:

.. code-block:: python

    from jiuwen.core.single_agent.agents import ReActAgent
    from jiuwen.core.foundation import OpenAIClient, ToolCard

    client = OpenAIClient.from_env()

    def search(query: str) -> str:
        return f"Results for '{query}'"

    agent = ReActAgent(
        client=client,
        tools=[
            ToolCard(name="search", description="Search the web",
                     parameters={"properties": {"query": {"type": "string"}}},
                     func=search),
        ],
        system_prompt="You are a helpful research assistant.",
    )

    result = await agent.run({"query": "What is the capital of France?"})

Output Format
-------------

The agent instructs the LLM to use this format:

.. code-block:: text

    Thought: your reasoning about what to do next
    Action: tool_name(param1=value1, param2=value2)
    Observation: the result of the action
    ... (repeat as needed)
    Thought: I now know the final answer
    Final Answer: the final answer to the user's question

Loop Safety
-----------

- **Max iterations**: defaults to 10, prevents infinite loops
- **Unknown format**: if LLM output doesn't match the pattern, agent prompts it to retry
- **Unknown tool**: returns an error Observation so LLM can adjust
