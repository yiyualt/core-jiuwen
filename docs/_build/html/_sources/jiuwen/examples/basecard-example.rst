BaseCard Examples
==================

Basic Construction
------------------

.. code-block:: python

    from jiuwen.core.common import BaseCard

    # Minimal: auto-generated ID
    card = BaseCard()
    print(card.id)   # e.g., "d4e5f6a7b8c9..."
    print(card.name)  # ""

    # With fields
    card = BaseCard(
        id="custom-id",
        name="search_agent",
        description="An agent that searches the web",
    )
    print(card.to_str())
    # id=custom-id,name=search_agent

Subclassing for Domain Cards
----------------------------

.. code-block:: python

    from typing import Any
    from jiuwen.core.common import BaseCard


    class AgentCard(BaseCard):
        """Card describing an AI agent."""
        version: str = "0.1.0"
        model: str = "default-model"
        max_tokens: int = 4096


    class ToolCard(BaseCard):
        """Card describing a callable tool."""
        version: str = "1.0"
        parameters: dict[str, Any] | None = None

        def tool_info(self) -> dict:
            return {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters or {},
            }

    # Create an agent card
    agent = AgentCard(
        name="chatbot",
        description="A conversational agent",
        model="gpt-4",
    )

    # Create a tool card
    tool = ToolCard(
        name="web_search",
        description="Search the web for information",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"],
        },
    )

    print(tool.tool_info())
    # {'name': 'web_search', 'description': 'Search the web for information',
    #  'parameters': {...}}

Serialization
-------------

.. code-block:: python

    from jiuwen.core.common import BaseCard

    card = BaseCard(
        id="abc123",
        name="export_test",
        description="Testing serialization",
    )

    # Python dict
    d = card.model_dump()
    print(d)
    # {'id': 'abc123', 'name': 'export_test', 'description': 'Testing serialization'}

    # JSON string
    json_str = card.model_dump_json()
    print(json_str)
    # {"id":"abc123","name":"export_test","description":"Testing serialization"}

Unique IDs Per Instance
-----------------------

.. code-block:: python

    from jiuwen.core.common import BaseCard

    # Each card gets a unique 32-character UUID hex
    cards = [BaseCard() for _ in range(3)]
    ids = {c.id for c in cards}
    print(len(ids))  # 3 — all unique
    print(len(cards[0].id))  # 32
