Runner + Agent Examples
=======================

End-to-End with Real LLM
-------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.runner import Runner
    from jiuwen.core.single_agent import WorkflowAgent, WorkflowAgentConfig
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig


    def create_poet_workflow():
        wf = Workflow()
        config = LLMCompConfig(
            template_content=[
                {"role": "system", "content": "You are a poet."},
                {"role": "user", "content": "Write a poem about {{topic}}"},
            ],
        )
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("poet", LLMComponent(config))
        wf.set_end_comp("end", End({"responseTemplate": "{{output}}"}))
        wf.add_connection("start", "poet")
        wf.add_connection("poet", "end")
        return wf


    async def main():
        agent = WorkflowAgent(WorkflowAgentConfig(
            id="poet", version="0.1", description="Writes poems",
        ))
        agent.add_workflows([create_poet_workflow()])

        result = await Runner.run_agent(agent, {"topic": "cherry blossoms"})
        print(result)

    asyncio.run(main())

Resource Manager
-----------------

.. code-block:: python

    import asyncio
    from jiuwen.core.runner import Runner
    from jiuwen.core.workflow import generate_workflow_key


    def create_weather_workflow():
        from jiuwen.core.workflow import Workflow, Start, End
        from jiuwen.core.foundation import ToolCard, ToolComponent
        from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

        def get_temp(city: str) -> str:
            return f"22C in {city}"

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("weather", ToolComponent(
            ToolCard(name="weather", func=get_temp)))
        wf.add_workflow_comp("llm", LLMComponent(LLMCompConfig(
            template_content=[{"role": "user", "content": "Weather: {{output}}. Summarize."}],
        )))
        wf.set_end_comp("end", End({"responseTemplate": "{{output}}"}))
        wf.add_connection("start", "weather")
        wf.add_connection("weather", "llm")
        wf.add_connection("llm", "end")
        return wf

    # Register for reuse
    Runner.resource_mgr.add_workflow(
        generate_workflow_key("weather_bot", "1.0"),
        create_weather_workflow,
    )

    # Later...
    wf = Runner.resource_mgr.get_workflow("weather_bot_1.0")

    async def main():
        from jiuwen.core.single_agent import WorkflowAgent, WorkflowAgentConfig
        agent = WorkflowAgent(WorkflowAgentConfig(id="weather_bot"))
        agent.add_workflows([wf])
        result = await Runner.run_agent(agent, {"city": "Paris"})
        print(result)

    asyncio.run(main())
