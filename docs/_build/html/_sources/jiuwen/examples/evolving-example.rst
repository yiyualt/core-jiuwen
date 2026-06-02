Agent Evolving Examples
=========================

This example shows a complete training loop using only ``FakeLLMClient``
(no real API needed). The default agent is deliberately poor at math and
geography — after training it improves to 100%.

.. code-block:: python

    import asyncio
    from jiuwen.core.agent_evolving import Case, Evaluator, Optimizer, Trainer
    from jiuwen.core.single_agent.agents import ReActAgent
    from tests.conftest import FakeLLMClient


    async def main():
        # ---- Step 1: Create a "dumb" agent ----
        # The default agent gives vague answers, so it fails many test cases.
        dumb_client = FakeLLMClient([
            "I don't know.",       # response for 2+2
            "Maybe somewhere?",    # response for capital
            "I think it's blue.",  # response for sky color (only correct one)
            "Not sure.",           # response for water boiling point
            "Final Answer: I'm not good at this.",  # training round 2
            "Final Answer: 4",     # response for 2+2 after training
            "Final Answer: Paris", # response for capital after training
            "Final Answer: blue",  # response for sky color after training
            "Final Answer: 100 degrees Celsius",  # response for boiling point after training
        ])
        agent = ReActAgent(client=dumb_client, system_prompt="You are helpful.")

        # ---- Step 2: Prepare test cases ----
        cases = [
            Case(input={"query": "What is 2+2?"}, expected="4"),
            Case(input={"query": "Capital of France?"}, expected="Paris"),
            Case(input={"query": "What color is the sky?"}, expected="blue"),
            Case(input={"query": "Boiling point of water?"}, expected="100"),
        ]

        # ---- Step 3: Create optimizer that generates better prompts ----
        optimizer_client = FakeLLMClient([
            "You are a precise assistant. Answer questions directly with the correct answer. Be specific.",
        ])
        optimizer = Optimizer(optimizer_client)

        evaluator = Evaluator(cases)
        trainer = Trainer(evaluator, optimizer, max_rounds=3)

        # ---- Step 4: Initial evaluation ----
        initial = await evaluator.evaluate(agent)
        print(f"Before training: {initial['score']:.0%} correct")

        # ---- Step 5: Train ----
        result = await trainer.train(agent)
        print(f"After training:  {result['best_score']:.0%} correct")
        print(f"Best prompt: {result['best_prompt']}")

        # ---- Step 6: Verify improvement ----
        assert result["best_score"] >= 1.0, "Training should reach 100%!"
        print("\\nTraining successfully improved the agent!")

    asyncio.run(main())


Expected output::

    Before training: 25% correct
    After training:  100% correct
    Best prompt: You are a precise assistant. Answer questions directly...
