Component Philosophy: Building Blocks
======================================

Components are the **reusable processing units** that make up a workflow.
Each component is an ``WorkflowComponent`` — a specialized ``Executable``
designed for ease of use.

Why WorkflowComponent?
----------------------

``WorkflowComponent`` adds a simpler interface on top of ``Executable``:

.. code-block:: python

    # Executable (raw)
    class MyNode(Executable[dict, dict]):
        async def on_invoke(self, inputs, **kwargs) -> dict:
            return process(inputs)

    # WorkflowComponent (simplified)
    class MyComponent(WorkflowComponent):
        async def invoke(self, inputs, **kwargs) -> dict:
            return process(inputs)

The ``WorkflowComponent`` simply delegates ``on_invoke`` → ``invoke``,
removing the need to remember the ``on_`` prefix.

Component Abilities (I/O Modes)
-------------------------------

Each component declares which I/O patterns it supports:

+------------------+------------------+-------------------------+-------------------+
| Ability          | Input            | Output                  | Typical Use       |
+==================+==================+=========================+===================+
| INVOKE           | batch (dict)     | batch (dict)            | Most components   |
+------------------+------------------+-------------------------+-------------------+
| STREAM           | batch (dict)     | async iterator          | Real-time output  |
+------------------+------------------+-------------------------+-------------------+
| COLLECT          | async iterator   | batch (dict)            | Aggregation       |
+------------------+------------------+-------------------------+-------------------+
| TRANSFORM        | async iterator   | async iterator          | Stream processing |
+------------------+------------------+-------------------------+-------------------+

v0.0.3 implements only INVOKE. Future versions add streaming support.

Built-in Components: Start and End
----------------------------------

**Start** — The simplest possible component:

.. code-block:: python

    class Start(WorkflowComponent):
        async def invoke(self, inputs, **kwargs):
            return inputs  # pass through

**End** — Collects results, optionally renders a template:

.. code-block:: python

    # Simple pass-through
    end = End()
    result = await end.invoke({"text": "hello"})
    # {"output": {"text": "hello"}}

    # With template
    end = End({"responseTemplate": "Result: {{output}}"})
    result = await end.invoke({"output": "world"})
    # {"response": "Result: world"}

Template Syntax
---------------

End component uses ``{{variable}}`` syntax (converted to Python
``string.Template`` internally):

- ``{{output}}`` → replaced with input's ``output`` value
- Missing variables → kept as ``$varname`` placeholder (safe substitution)
