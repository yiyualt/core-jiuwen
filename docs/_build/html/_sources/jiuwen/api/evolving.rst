``jiuwen.core.agent_evolving``
================================

.. module:: jiuwen.core.agent_evolving

Case
----

.. class:: Case(input: dict, expected: str, metadata: dict = {})

   A test case for agent evaluation.

Evaluator
---------

.. class:: Evaluator(cases: list[Case])

   .. method:: async evaluate(agent) -> dict

       Returns {"score": float, "results": [...]}.

Optimizer
---------

.. class:: Optimizer(client: LLMClient)

   .. method:: async optimize(current_prompt: str, failures: list) -> str

Trainer
-------

.. class:: Trainer(evaluator: Evaluator, optimizer: Optimizer, max_rounds: int = 5)

   .. method:: async train(agent) -> dict

       Returns {"best_prompt": str, "best_score": float, "history": [...]}.
