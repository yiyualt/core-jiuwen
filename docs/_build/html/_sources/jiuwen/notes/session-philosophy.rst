Session: Multi-Turn Memory
===========================

A ``Session`` gives agents memory across multiple invocations.
Without it, each ``agent.run()`` is a clean slate.

Without Session
---------------

.. code-block:: python

    result1 = await agent.run({"query": "I'm Bob"})
    # "Nice to meet you, Bob!"

    result2 = await agent.run({"query": "What's my name?"})
    # "I don't know your name."  ← forgot!

With Session
------------

.. code-block:: python

    session = Session()

    result1 = await agent.run({"query": "I'm Bob"}, session=session)
    # "Nice to meet you, Bob!"

    result2 = await agent.run({"query": "What's my name?"}, session=session)
    # "Your name is Bob."  ← remembered!

How It Works
------------

Session stores messages in a list:

.. code-block:: text

    Session
    ├── _messages: [{"role": "user", "content": "I'm Bob"},
    │               {"role": "assistant", "content": "Nice to meet you, Bob!"}]
    └── _state: {}  (arbitrary key-value storage)

When an agent runs with a session:
1. User message is added to session
2. Session history is injected into the LLM prompt
3. Agent response is added to session

Streaming
---------

``StreamEmitter`` enables real-time output:

.. code-block:: python

    async for chunk in agent.stream({"query": "Research AI"}, session=session):
        if chunk["type"] == "action":
            print(f"[Tool] {chunk['data']}")
        elif chunk["type"] == "final":
            print(f"[Answer] {chunk['data']}")
