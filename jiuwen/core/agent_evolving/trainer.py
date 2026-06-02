# coding: utf-8
"""Trainer — iterative prompt optimization loop."""

from typing import Any

from jiuwen.core.agent_evolving.evaluator import Evaluator
from jiuwen.core.agent_evolving.optimizer import Optimizer


class Trainer:
    """Iteratively improves an agent's prompt through evaluation and optimization.

    Usage::

        evaluator = Evaluator(cases)
        optimizer = Optimizer(client)
        trainer = Trainer(evaluator, optimizer, max_rounds=5)

        result = await trainer.train(agent)
        print(result["best_prompt"])
        print(result["best_score"])
    """

    def __init__(self, evaluator: Evaluator, optimizer: Optimizer, max_rounds: int = 5):
        self._evaluator = evaluator
        self._optimizer = optimizer
        self._max_rounds = max_rounds

    async def train(self, agent: Any) -> dict[str, Any]:
        """Run the training loop.

        Args:
            agent: An agent with agent._system_prompt attribute that can be modified.

        Returns:
            Dict with "best_prompt", "best_score", "history" (list of round results).
        """
        best_prompt = getattr(agent, '_system_prompt', '')
        best_score = 0.0
        history = []

        for round_num in range(1, self._max_rounds + 1):
            result = await self._evaluator.evaluate(agent)
            score = result["score"]
            history.append({"round": round_num, "score": score, "prompt": best_prompt})

            if score > best_score:
                best_score = score
                best_prompt = getattr(agent, '_system_prompt', '')

            if score >= 1.0:
                break

            failures = [r for r in result["results"] if not r["passed"]]
            if failures:
                new_prompt = await self._optimizer.optimize(best_prompt, failures)
                try:
                    agent._system_prompt = new_prompt
                except AttributeError:
                    pass

        history.append({"round": "final", "score": best_score, "prompt": best_prompt})
        return {"best_prompt": best_prompt, "best_score": best_score, "history": history}
