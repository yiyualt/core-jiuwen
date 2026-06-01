LLM Component: AI in the Pipeline
==================================

The ``LLMComponent`` is the bridge between ``LLMClient`` (v0.0.4) and
``Workflow`` (v0.0.3). It wraps ``OpenAIClient`` into a workflow node.

Setup: create a ``.env`` file (copy from ``.env.example``) with your API key.

Zero-Config Usage
-----------------

With a ``.env`` file configured, LLMComponent works out of the box:

.. code-block:: python

    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

    config = LLMCompConfig(
        template_content=[
            {"role": "user", "content": "{{query}}"},
        ],
    )
    comp = LLMComponent(config)  # auto-detects OpenAIClient from .env

    result = await comp.invoke({"query": "What is AI?"})
    print(result["output"])

Explicit Client
---------------

Or pass a client directly for custom setup:

.. code-block:: python

    from jiuwen.core.foundation import OpenAIClient
    client = OpenAIClient.from_env()
    comp = LLMComponent(config, client)

Template Prompt System
----------------------

LLMComponent uses ``{{variable}}`` template syntax:

.. code-block:: python

    config = LLMCompConfig(
        template_content=[
            {"role": "system", "content": "你是{{role}}。"},
            {"role": "user", "content": "{{query}}"},
        ],
    )

    # inputs: {"role": "翻译官", "query": "翻译: hello"}
    # → messages: [{"role": "system", "content": "你是翻译官。"},
    #              {"role": "user", "content": "翻译: hello"}]

Streaming
---------

.. code-block:: python

    async for chunk in comp.stream({"query": "Tell a story"}):
        print(chunk["output"], end="", flush=True)
