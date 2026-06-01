Workflow Philosophy: Composing Components
=========================================

A Workflow is a **directed graph of components** that process data
through a pipeline. It's the orchestration layer that turns individual
components (LLM calls, transformations, tools) into a complete
application.

The Anatomy of a Workflow
-------------------------

.. code-block:: text

    Workflow
    ├── WorkflowCard     ← "who am I?" (identity)
    ├── PregelGraph      ← "how do I run?" (execution engine)
    └── Components       ← "what do I do?" (processing nodes)

    Execution Flow:
    ┌───────┐     ┌───────┐     ┌───────┐
    │ Start │────▶│  LLM  │────▶│  End  │
    └───────┘     └───────┘     └───────┘
    (entry)      (process)      (exit)

Three Roles of Components
-------------------------

- **Start**: Entry point, passes inputs through unchanged
- **Intermediate**: Processes data (e.g., LLM call, transformation)
- **End**: Exit point, wraps output and optionally renders a template

Card/Config in Workflows
------------------------

``WorkflowCard`` extends ``BaseCard`` with workflow-specific metadata:

.. code-block:: python

    card = WorkflowCard(
        id="text_generator",
        name="Text Generator",
        version="2.0",
        input_params={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    )

The ``version`` field enables multiple versions of the same workflow
to coexist. The ``input_params`` defines the expected input schema
as a JSON Schema object — useful for tool-calling systems and validation.

Lifecycle: Build → Compile → Run
---------------------------------

1. **Build**: Register components and connect them
2. **Compile**: Translate to executable graph (PregelGraph)
3. **Run**: Execute with input data

.. code-block:: python

    wf = Workflow(card)
    wf.set_start_comp("entry", Start())
    wf.set_end_comp("exit", End())
    wf.add_connection("entry", "exit")

    result = await wf.invoke({"query": "hello"})
    # WorkflowOutput(result=..., state=COMPLETED)
