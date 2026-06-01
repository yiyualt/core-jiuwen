Runner: The Entry Point
========================

The ``Runner`` is jiuwen's global execution entry point. It provides
a unified interface for running agents and managing resources.

Why a Runner?
-------------

Before Runner, you called ``wf.invoke()`` directly on a Workflow instance.
This works but doesn't scale:

- **Discovery**: How do other parts of the system find your workflows?
- **Sharing**: How do you reuse the same workflow across agents?
- **Lifecycle**: Who owns the workflow instances?

Runner solves this with a **process-global registry**:

.. code-block:: python

    from jiuwen.core.runner import Runner
    from jiuwen.core.workflow import generate_workflow_key

    # Register a workflow
    Runner.resource_mgr.add_workflow(
        generate_workflow_key("text_gen", "1.0"),
        lambda: create_text_workflow(),
    )

    # Later, retrieve and use
    wf = Runner.resource_mgr.get_workflow("text_gen_1.0")

ResourceManager
---------------

``Runner.resource_mgr`` is a ``ResourceManager`` instance that stores:

- **Workflows**: registered by key (id_version), stored as factory functions for lazy instantiation
- **Tools**: tool metadata cards, indexed by name

Usage Pattern
-------------

.. code-block:: python

    from jiuwen.core.runner import Runner
    from jiuwen.core.single_agent import WorkflowAgent, WorkflowAgentConfig

    # 1. Create agent
    agent = WorkflowAgent(WorkflowAgentConfig(id="my_agent"))
    agent.add_workflows([wf])

    # 2. Execute via Runner
    result = await Runner.run_agent(agent, {"query": "hello"})
