# coding: utf-8
"""Tests for Case, Evaluator, Optimizer, and Trainer."""

import pytest
from tests.conftest import FakeLLMClient
from jiuwen.core.agent_evolving import Case, Evaluator, Optimizer, Trainer


class TestCase:
    def test_construction(self):
        c = Case(input={"query": "2+2"}, expected="4")
        assert c.input == {"query": "2+2"}
        assert c.expected == "4"

    def test_metadata(self):
        c = Case(input={"q": "x"}, expected="y", metadata={"source": "test"})
        assert c.metadata["source"] == "test"


class TestEvaluator:
    @pytest.mark.asyncio
    async def test_perfect_score(self):
        class PerfectAgent:
            async def run(self, inputs, session=None):
                return {"result": "4"}

        cases = [Case(input={"query": "2+2"}, expected="4")]
        result = await Evaluator(cases).evaluate(PerfectAgent())
        assert result["score"] == 1.0

    @pytest.mark.asyncio
    async def test_partial_score(self):
        class PartialAgent:
            def __init__(self):
                self.call_count = 0

            async def run(self, inputs, session=None):
                self.call_count += 1
                return {"result": "4" if self.call_count == 1 else "wrong"}

        cases = [
            Case(input={"q": "2+2"}, expected="4"),
            Case(input={"q": "3+3"}, expected="6"),
        ]
        result = await Evaluator(cases).evaluate(PartialAgent())
        assert result["score"] == 0.5

    @pytest.mark.asyncio
    async def test_agent_error_handled(self):
        class BrokenAgent:
            async def run(self, inputs, session=None):
                raise RuntimeError("fail")

        cases = [Case(input={"q": "test"}, expected="x")]
        result = await Evaluator(cases).evaluate(BrokenAgent())
        assert result["score"] == 0.0


class TestOptimizer:
    @pytest.mark.asyncio
    async def test_generates_new_prompt(self):
        client = FakeLLMClient(["Be precise. Answer with numbers only."])
        optimizer = Optimizer(client)

        failures = [{"case": Case(input={"q": "2+2"}, expected="4"), "actual": "the answer is four"}]
        new_prompt = await optimizer.optimize("You are helpful.", failures)
        assert new_prompt != "You are helpful."

    @pytest.mark.asyncio
    async def test_no_failures_returns_original(self):
        optimizer = Optimizer(FakeLLMClient(["ignored"]))
        result = await optimizer.optimize("original prompt", [])
        assert result == "original prompt"


class TestTrainer:
    @pytest.mark.asyncio
    async def test_training_loop(self):
        class TrainableAgent:
            def __init__(self):
                self._system_prompt = "You are helpful."

            async def run(self, inputs, session=None):
                q = inputs.get("query", "")
                if "optimized" in self._system_prompt:
                    return {"result": "4" if "2+2" in q else "6"}
                return {"result": "wrong"}

        agent = TrainableAgent()
        cases = [
            Case(input={"query": "2+2"}, expected="4"),
            Case(input={"query": "3+3"}, expected="6"),
        ]
        evaluator = Evaluator(cases)

        # Optimizer adds "optimized" to the prompt
        client = FakeLLMClient(["You are helpful optimized."])
        optimizer = Optimizer(client)

        trainer = Trainer(evaluator, optimizer, max_rounds=3)
        result = await trainer.train(agent)

        assert result["best_score"] == 1.0
        assert "optimized" in result["best_prompt"]

    @pytest.mark.asyncio
    async def test_perfect_from_start(self):
        class PerfectAgent:
            _system_prompt = "perfect"

            async def run(self, inputs, session=None):
                return {"result": "4"}

        agent = PerfectAgent()
        evaluator = Evaluator([Case(input={"q": "2+2"}, expected="4")])
        optimizer = Optimizer(FakeLLMClient(["ignored"]))
        trainer = Trainer(evaluator, optimizer, max_rounds=3)

        result = await trainer.train(agent)
        assert result["best_score"] == 1.0
