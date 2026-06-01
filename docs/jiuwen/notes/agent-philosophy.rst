Agent: The Intelligent Interface
================================

An **Agent** is the user-facing abstraction in jiuwen. It bundles
workflows, tools, and configuration into a single runnable unit.

AgentCard
---------

``AgentCard`` is the metadata identity for an agent:

.. code-block:: python

    card = AgentCard(
        id="assistant",
        name="AI Assistant",
        version="0.1.0",
        model="gpt-4o",
        description="A helpful AI assistant",
    )

WorkflowAgent
-------------

``WorkflowAgent`` is the primary agent type. It binds one or more
workflows and executes them on demand:

.. code-block:: python

    from jiuwen.core.single_agent import WorkflowAgent, WorkflowAgentConfig

    config = WorkflowAgentConfig(
        id="poet_agent",
        version="0.1",
        description="Writes poems on request",
    )
    agent = WorkflowAgent(config)
    agent.add_workflows([poem_workflow])

    # Run directly
    result = await agent.run({"topic": "spring"})

    # Or via Runner
    from jiuwen.core.runner import Runner
    result = await Runner.run_agent(agent, {"topic": "spring"})

Multiple Workflows
------------------

An agent can bind multiple workflows. Each is executed in order,
and results are combined:

.. code-block:: python

    agent.add_workflows([translate_wf, summarize_wf])
    result = await agent.run({"text": "..."})
    # result["results"] = {"translate_wf_1.0": ..., "summarize_wf_1.0": ...}
