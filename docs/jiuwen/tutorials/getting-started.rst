Getting Started
================

This guide walks you through installing jiuwen and creating your first
``BaseCard``.

Installation
------------

.. code-block:: bash

    pip install -e .

Or with uv:

.. code-block:: bash

    uv sync

Your First BaseCard
-------------------

``BaseCard`` is the foundational building block of jiuwen. Every agent,
tool, and workflow uses metadata cards that inherit from it.

.. code-block:: python

    from jiuwen.core.common import BaseCard

    # Create a card with auto-generated ID
    card = BaseCard(name="my_agent", description="My first agent")

    print(card.id)          # e.g., "a1b2c3d4..."
    print(card.name)        # "my_agent"
    print(card.to_str())    # "id=a1b2c3d4...,name=my_agent"

Subclassing BaseCard
--------------------

Create your own card types by extending ``BaseCard``:

.. code-block:: python

    from jiuwen.core.common import BaseCard
    from pydantic import Field

    class ToolCard(BaseCard):
        version: str = "0.1.0"
        parameters: dict | None = None

        def tool_info(self):
            return {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters or {},
            }

Serialization
-------------

All cards are Pydantic models and can be serialized:

.. code-block:: python

    card = BaseCard(name="test", description="A test card")

    # To dict
    data = card.model_dump()
    # {"id": "...", "name": "test", "description": "A test card"}

    # To JSON
    json_str = card.model_dump_json()

Next Steps
----------

- :doc:`/jiuwen/notes/basecard-philosophy` — understand the Card/Config split
- :doc:`/jiuwen/examples/basecard-example` — more usage examples
- :doc:`/jiuwen/api/common` — API reference
