Task Loop Examples
===================

Observable Execution
--------------------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.core.single_agent.agents import ReActAgent
    from jiuwen.harness.task_loop import TaskExecutor, LoggingHandler


    async def main():
        # Create a simple agent
        agent = ReActAgent(client=FakeLLMClient(["Final Answer: Fixed!"]))

        # Wrap with event-emitting executor
        executor = TaskExecutor(agent, handlers=[LoggingHandler()])

        # Execute — events are printed to stderr in real-time
        result = await executor.execute("Fix the null pointer bug")
        print(f"Result: {result['result']}")

    asyncio.run(main())

    # Output:
    # [task_start] {'task': 'Fix the null pointer bug'}
    # [task_complete] {'result': 'Fixed!'}
    # Result: Fixed!

Custom Event Handler
--------------------

.. code-block:: python

    import asyncio
    from jiuwen.harness.task_loop import TaskExecutor, EventHandler, TaskEvent


    class ProgressHandler(EventHandler):
        """Shows a spinner while the agent works."""
        async def on_event(self, event: TaskEvent):
            if event.type == "task_start":
                print(f"  Working...")
            elif event.type == "task_complete":
                print(f"  Done!")
            elif event.type == "error":
                print(f"  Failed: {event.data['error']}")


    async def main():
        from tests.conftest import FakeLLMClient
        from jiuwen.core.single_agent.agents import ReActAgent

        agent = ReActAgent(client=FakeLLMClient(["Final Answer: Done"]))
        executor = TaskExecutor(agent, handlers=[ProgressHandler()])
        await executor.execute("Optimize the code")

    asyncio.run(main())

Batch Task Queue
----------------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.core.single_agent.agents import ReActAgent
    from jiuwen.harness.task_loop import TaskExecutor, LoopCoordinator, EventHandler


    class CollectHandler(EventHandler):
        def __init__(self):
            self.completed = []

        async def on_event(self, event):
            if event.type == "task_complete":
                self.completed.append(event.data["result"])


    async def main():
        agent = ReActAgent(client=FakeLLMClient(["Done"]))
        handler = CollectHandler()
        executor = TaskExecutor(agent, handlers=[handler])
        coordinator = LoopCoordinator(executor)

        # Submit a batch of tasks
        tasks = ["Add logging", "Fix typo", "Update docs"]
        for t in tasks:
            await coordinator.submit(t)
        await coordinator.submit(None)  # stop

        await coordinator.run()
        print(f"Completed {len(handler.completed)} tasks")
        # Completed 3 tasks

    asyncio.run(main())
