Agent Evolving: Automatic Prompt Optimization
================================================

The **Agent Evolving** system automatically improves an agent's
system prompt through iterative evaluation and optimization.

How It Works
------------

.. code-block:: text

    ┌────────────────────────────────────────────┐
    │             Training Loop                   │
    │                                            │
    │  1. Evaluate agent on test cases           │
    │     ┌──────────┐                           │
    │     │Evaluator │ → score, failures          │
    │     └──────────┘                           │
    │          │                                  │
    │          ▼                                  │
    │  2. If score = 1.0 → STOP                  │
    │     Otherwise → analyze failures            │
    │          │                                  │
    │          ▼                                  │
    │  3. Generate improved prompt                │
    │     ┌──────────┐                           │
    │     │Optimizer │ → new prompt               │
    │     └──────────┘                           │
    │          │                                  │
    │          ▼                                  │
    │  4. Update agent, repeat from step 1        │
    │                                            │
    └────────────────────────────────────────────┘

Usage
-----

.. code-block:: python

    from jiuwen.core.agent_evolving import Case, Evaluator, Optimizer, Trainer
    from jiuwen.core.foundation import OpenAIClient

    # Prepare test cases
    cases = [
        Case(input={"query": "2+2"}, expected="4"),
        Case(input={"query": "Capital of France?"}, expected="Paris"),
    ]

    # Create trainer
    client = OpenAIClient.from_env()
    evaluator = Evaluator(cases)
    optimizer = Optimizer(client)
    trainer = Trainer(evaluator, optimizer, max_rounds=5)

    # Train
    result = await trainer.train(agent)
    agent._system_prompt = result["best_prompt"]
    print(f"Best score: {result['best_score']}, Prompt: {result['best_prompt']}")
