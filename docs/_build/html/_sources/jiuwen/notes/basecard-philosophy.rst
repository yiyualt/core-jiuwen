BaseCard Philosophy: The Card/Config Split
==========================================

Design Intent
-------------

jiuwen follows a strict **Card/Config separation** pattern. Understanding
this split is key to using the SDK effectively.

.. list-table:: Card vs Config
   :header-rows: 1

   * - Property
     - **Card** (metadata)
     - **Config** (runtime)
   * - Purpose
     - Describe identity
     - Hold behavior and state
   * - Serialization
     - Yes (JSON, cross-process)
     - No (process-local)
   * - Mutability
     - Immutable after creation
     - Mutable during runtime
   * - Examples
     - ``WorkflowCard``, ``ToolCard``, ``AgentCard``
     - ``WorkflowConfig``, ``RunnerConfig``

Why Split?
----------

**1. Transportability.** Cards can cross process boundaries (e.g., A2A protocol,
REST APIs) because they contain only serializable metadata — no runtime
references, no open connections, no mutable state.

**2. Discovery.** A registry can enumerate available capabilities by
inspecting Cards without loading the corresponding runtime Configs.

**3. Safety.** Cards are immutable. Two components can share a Card
reference without risk of one component corrupting another's state.

The BaseCard Class
------------------

``BaseCard`` is the root of the Card hierarchy:

.. code-block:: python

    class BaseCard(BaseModel):
        id: str = Field(default_factory=lambda: uuid.uuid4().hex)
        name: str = Field(default="")
        description: str = Field(default="")

Three fields define every Card:

- **id**: A UUID hex string. Auto-generated if not provided. Used for
  registration and lookups.
- **name**: A human-readable identifier. Must be unique within its
  namespace (e.g., all workflows in a runner).
- **description**: Free-form text describing the card's purpose and
  capabilities.

The ``tool_info()`` method
--------------------------

Cards expose a ``tool_info()`` method that returns structured metadata
for tool-calling systems:

.. code-block:: python

    class WorkflowCard(BaseCard):
        version: str = ""
        input_params: dict | None = None

        def tool_info(self):
            return {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_params or {},
            }

This allows LLM tool-calling frameworks to discover and invoke
capabilities without knowing about specific Card subclasses.

Anti-Patterns
-------------

- **Don't** put ``session_id``, ``runner`` references, or other runtime
  data in a Card. That belongs in a Config.
- **Don't** define static description fields in a Config. That belongs
  in a Card.
- **Don't** inject dynamic computation into a Card's serialization
  methods. Cards should be pure data.
