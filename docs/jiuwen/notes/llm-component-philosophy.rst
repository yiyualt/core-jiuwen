LLM Component: AI in the Pipeline
==================================

The ``LLMComponent`` is the bridge between ``LLMClient`` (v0.0.4) and
``Workflow`` (v0.0.3). It wraps an LLM call into a standard workflow
component that can be placed anywhere in a pipeline.

Architecture
------------

.. code-block:: text

    LLMComponent
    ├── LLMCompConfig         ← what to do
    │   ├── model_client_config  (connection)
    │   ├── model_config         (request params)
    │   ├── template_content     (prompt template)
    │   └── output_config        (expected output schema)
    └── LLMClient             ← how to do it
        (FakeLLMClient in tests)

Template Prompt System
----------------------

LLMComponent uses ``{{variable}}`` template syntax. At invoke time,
variables are replaced with values from the inputs dict:

.. code-block:: python

    config = LLMCompConfig(
        template_content=[
            {"role": "system", "content": "你是一个{{role}}。"},
            {"role": "user", "content": "{{query}}"},
        ],
        ...
    )

    # inputs: {"role": "翻译官", "query": "翻译: hello"}
    # → messages: [{"role": "system", "content": "你是一个翻译官。"},
    #              {"role": "user", "content": "翻译: hello"}]

Testing with FakeLLMClient
--------------------------

LLMComponent defaults to ``FakeLLMClient`` if no client is provided,
making it testable out of the box:

.. code-block:: python

    from jiuwen.core.foundation import FakeLLMClient
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

    client = FakeLLMClient(["Bonjour!"])
    config = LLMCompConfig(
        template_content=[{"role": "user", "content": "{{text}}"}],
    )
    comp = LLMComponent(config, client)
    result = await comp.invoke({"text": "Translate: hello"})
    assert result["output"] == "Bonjour!"

Streaming Support
-----------------

For real-time output, use ``stream()`` instead of ``invoke()``:

.. code-block:: python

    async for chunk in comp.stream({"query": "Tell a story"}):
        print(chunk["output"], end="", flush=True)
