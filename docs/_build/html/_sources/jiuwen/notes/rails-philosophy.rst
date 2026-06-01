Rails: Composable Agent Middleware
=====================================

Rails are composable before/after hooks that wrap agent execution.
Think of them as middleware for AI agents.

Pipeline Architecture
---------------------

.. code-block:: text

    Request → [Rail A.before] → [Rail B.before] → Agent.run
                                                    ↓
    Response ← [Rail A.after] ← [Rail B.after] ← ───┘

Each rail can:
- **Inspect** inputs/outputs
- **Modify** data flowing through
- **Block** execution (short-circuit with a response)

Built-in Rails
--------------

**SecurityRail** — blocks dangerous patterns:

.. code-block:: python

    from jiuwen.core.rails import SecurityRail

    rail = SecurityRail()
    result = await rail.before({"query": "DROP TABLE users"})
    # {"result": "Blocked: dangerous content detected (matched: 'drop table')"}

Custom Rails
------------

.. code-block:: python

    from jiuwen.core.rails import BaseRail

    class LoggingRail(BaseRail):
        async def before(self, inputs, session=None):
            print(f"[LOG] Agent called: {inputs}")
            return inputs

        async def after(self, result, session=None):
            print(f"[LOG] Agent returned: {result}")
            return result

Integration with Runner
-----------------------

Add rails to Runner for automatic filtering:

.. code-block:: python

    from jiuwen.core.runner import Runner
    from jiuwen.core.rails import SecurityRail

    Runner.rails.add_rail(SecurityRail())

    # All agent calls through Runner are now filtered
    result = await Runner.run_agent(agent, {"query": "..."})
