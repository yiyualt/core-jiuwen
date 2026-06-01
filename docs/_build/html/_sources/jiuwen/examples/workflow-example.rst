Workflow Examples
=================

Minimal Pipeline: Start → End
-------------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow import Workflow, Start, End

    wf = Workflow()
    wf.set_start_comp("entry", Start())
    wf.set_end_comp("exit", End())
    wf.add_connection("entry", "exit")

    result = asyncio.run(wf.invoke({"message": "hello world"}))
    print(result.state)   # COMPLETED

Three-Component Pipeline
------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow import Workflow, Start, End, WorkflowComponent


    class UppercaseComponent(WorkflowComponent):
        """A custom component that uppercases text."""
        async def invoke(self, inputs: dict, **kwargs) -> dict:
            text = inputs.get("text", inputs.get("output", ""))
            return {"output": text.upper()}


    wf = Workflow()
    wf.set_start_comp("start", Start())
    wf.add_workflow_comp("upper", UppercaseComponent())
    wf.set_end_comp("end", End({"responseTemplate": "Result: {{output}}"}))

    wf.add_connection("start", "upper")
    wf.add_connection("upper", "end")

    result = asyncio.run(wf.invoke({"text": "hello world"}))
    print(result.result)
    # {"response": "Result: HELLO WORLD"}

Using WorkflowCard with Metadata
---------------------------------

.. code-block:: python

    from jiuwen.core.workflow import Workflow, WorkflowCard

    card = WorkflowCard(
        id="text_processor",
        name="Text Processing Pipeline",
        version="1.0",
        description="Uppercases input text",
        input_params={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    )

    wf = Workflow(card)
    print(wf.card.tool_info())
    # {'name': 'Text Processing Pipeline', 'description': '...', 'parameters': {...}}

Error Handling
--------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow import Workflow, WorkflowComponent

    class FailingComponent(WorkflowComponent):
        async def invoke(self, inputs: dict, **kwargs) -> dict:
            raise ValueError("Something went wrong")

    wf = Workflow()
    wf.set_start_comp("fail", FailingComponent())
    wf.set_end_comp("fail", FailingComponent())

    result = asyncio.run(wf.invoke({}))
    print(result.state)    # ERROR
    print(result.result)   # None
