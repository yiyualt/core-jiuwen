# coding: utf-8
"""Evaluator — scores an agent against a dataset."""

from typing import Any

from jiuwen.core.agent_evolving.dataset import Case


class Evaluator:
    """Evaluates an agent's performance on a dataset.

    Usage::

        cases = [Case(input={"query": "2+2"}, expected="4"), ...]
        evaluator = Evaluator(cases)
        result = await evaluator.evaluate(agent)
        print(result["score"])  # 0.0 to 1.0
    """

    def __init__(self, cases: list[Case]):
        self._cases = cases

    @property
    def cases(self) -> list[Case]:
        return list(self._cases)

    async def evaluate(self, agent: Any) -> dict[str, Any]:
        """Run the agent on all cases and compute accuracy.

        Args:
            agent: An agent with async run(inputs) → dict method.

        Returns:
            Dict with "score" (float 0-1) and "results" (list of per-case dicts).
        """
        results = []
        for case in self._cases:
            try:
                output = await agent.run(case.input)
                actual = str(output.get("result", ""))
            except Exception as e:
                actual = f"ERROR: {e}"

            passed = case.expected.lower() in actual.lower()
            results.append({
                "case": case,
                "passed": passed,
                "actual": actual,
            })

        score = sum(1 for r in results if r["passed"]) / len(results) if results else 0.0
        return {"score": score, "results": results}
