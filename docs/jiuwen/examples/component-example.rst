Component Examples
===================

Creating Custom Components
--------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow.components import WorkflowComponent


    class AdderComponent(WorkflowComponent):
        """Adds two numbers from the input."""
        async def invoke(self, inputs: dict, **kwargs) -> dict:
            a = inputs.get("a", 0)
            b = inputs.get("b", 0)
            return {"sum": a + b}


    class MultiplierComponent(WorkflowComponent):
        """Multiplies two numbers."""
        async def invoke(self, inputs: dict, **kwargs) -> dict:
            x = inputs.get("x", 1)
            y = inputs.get("y", 1)
            return {"product": x * y}


    # Use components directly
    adder = AdderComponent()
    result = asyncio.run(adder.invoke({"a": 3, "b": 4}))
    print(result)  # {"sum": 7}

Streaming Component
-------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow.components import WorkflowComponent


    class WordSplitter(WorkflowComponent):
        """Splits input text into words, yielding one at a time."""
        async def stream(self, inputs: dict, **kwargs):
            text = inputs.get("text", "")
            for word in text.split():
                yield {"word": word}


    async def main():
        splitter = WordSplitter()
        async for chunk in splitter.stream({"text": "hello world test"}):
            print(chunk)
        # {"word": "hello"}
        # {"word": "world"}
        # {"word": "test"}

    asyncio.run(main())

Component Metadata
------------------

.. code-block:: python

    from jiuwen.core.workflow.components import (
        ComponentConfig, WorkflowComponentMetadata
    )

    # Describe a component instance
    meta = WorkflowComponentMetadata(
        node_id="llm_node_1",
        node_type="LLM",
        node_name="ChatGPT Caller",
    )

    config = ComponentConfig(metadata=meta)
    print(config.metadata.node_id)   # "llm_node_1"
    print(config.metadata.node_type) # "LLM"
