Tool System: Functions as Components
=====================================

The Tool System wraps Python functions into Workflow components.
With ``ToolCard`` and ``ToolComponent``, any function becomes a
reusable building block that can be placed in a pipeline.

ToolCard: Identity for Functions
--------------------------------

``ToolCard`` extends ``BaseCard`` with two additions:

- **parameters**: JSON Schema describing inputs
- **func**: The actual Python callable

The ``func`` is excluded from serialization — cards can be shared
as metadata without exposing implementation:

.. code-block:: python

    def search(query: str) -> list[str]:
        return ["result1", "result2"]

    card = ToolCard(
        name="web_search",
        description="Search the web",
        parameters={"query": {"type": "string"}},
        func=search,
    )

    # Serialize for discovery
    metadata = card.model_dump()
    # {"id": "...", "name": "web_search", "parameters": {...}}
    # func is NOT included

Sync and Async Tools
--------------------

``ToolComponent.invoke`` automatically detects sync vs async:

.. code-block:: python

    # Sync function
    def add(a: int, b: int) -> int:
        return a + b

    # Async function
    async def fetch(url: str) -> dict:
        return await http_get(url)

    # Both work the same way:
    comp = ToolComponent(ToolCard(name="...", func=add))
    result = await comp.invoke({"a": 3, "b": 4})
    # {"output": 7}

LLM + Tool Pipelines
--------------------

The real power comes from combining LLM and Tool:

.. code-block:: text

    ┌───────┐   ┌──────────┐   ┌──────────┐   ┌───────┐
    │ Start │──▶│   Tool   │──▶│   LLM    │──▶│  End  │
    └───────┘   │ (weather)│   │ (report) │   └───────┘
                └──────────┘   └──────────┘

Tool runs first (fetch weather data), then LLM formats it nicely.
