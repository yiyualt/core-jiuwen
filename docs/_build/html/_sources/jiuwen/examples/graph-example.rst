Graph Examples
==============

Building a Simple Pipeline
--------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.graph import Executable, PregelGraph


    class UpperNode(Executable):
        """A node that uppercases its input."""
        async def on_invoke(self, inputs: dict, **kwargs) -> dict:
            text = inputs.get("text", "")
            return {"text": text.upper()}


    class PrefixNode(Executable):
        """A node that adds a prefix."""
        async def on_invoke(self, inputs: dict, **kwargs) -> dict:
            text = inputs.get("text", "")
            return {"text": f"Result: {text}"}

    # Build the graph
    graph = PregelGraph()
    graph.add_node("upper", UpperNode())
    graph.add_node("prefix", PrefixNode())
    graph.add_edge("upper", "prefix")
    graph.start_node("upper")
    graph.end_node("prefix")

    # Compile and run
    compiled = graph.compile()
    result = asyncio.run(compiled._invoke({"text": "hello world"}))
    print(result)  # {"prefix": {"text": "Result: HELLO WORLD"}}


Fan-Out: One Node Triggers Many
--------------------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.graph import Executable, PregelGraph


    class EchoNode(Executable):
        def __init__(self, label: str):
            self.label = label

        async def on_invoke(self, inputs: dict, **kwargs) -> dict:
            return {self.label: f"processed by {self.label}"}

    # Two workers start concurrently
    graph = PregelGraph()
    graph.add_node("worker_a", EchoNode("a"))
    graph.add_node("worker_b", EchoNode("b"))
    graph.start_node("worker_a")
    graph.start_node("worker_b")
    # Both run in parallel — no dependencies between them

    result = asyncio.run(graph.compile()._invoke({"task": "process"}))
    # Both workers output their results


Creating a Custom Executable
----------------------------

.. code-block:: python

    from typing import AsyncIterator
    from jiuwen.core.graph import Executable


    class StreamingNode(Executable[dict, str]):
        """A node that demonstrates the stream interface."""

        async def on_invoke(self, inputs: dict, **kwargs) -> dict:
            words = inputs.get("text", "").split()
            return {"count": len(words), "words": words}

        async def on_stream(self, inputs: dict, **kwargs) -> AsyncIterator[str]:
            for word in inputs.get("text", "").split():
                yield word
