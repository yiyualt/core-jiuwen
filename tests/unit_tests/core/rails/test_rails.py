# coding: utf-8
"""Tests for BaseRail, RailPipeline, and SecurityRail."""

import pytest
from jiuwen.core.rails.base import BaseRail, RailPipeline
from jiuwen.core.rails.security_rail import SecurityRail


class LoggingRail(BaseRail):
    def __init__(self):
        self.before_calls = 0
        self.after_calls = 0

    async def before(self, inputs, session=None):
        self.before_calls += 1
        inputs["_logged"] = True
        return inputs

    async def after(self, result, session=None):
        self.after_calls += 1
        result["_audited"] = True
        return result


class TestBaseRail:
    @pytest.mark.asyncio
    async def test_default_pass_through(self):
        rail = BaseRail()
        assert await rail.before({"x": 1}) == {"x": 1}
        assert await rail.after({"y": 2}) == {"y": 2}


class TestRailPipeline:
    @pytest.mark.asyncio
    async def test_execution_order(self):
        class SpyAgent:
            async def run(self, inputs, session=None):
                return {"result": f"processed: {inputs}"}

        log1 = LoggingRail()
        log2 = LoggingRail()
        pipeline = RailPipeline([log1, log2])

        agent = SpyAgent()
        result = await pipeline.run(agent, {"msg": "hello"})

        assert log1.before_calls == 1
        assert log2.before_calls == 1
        assert log1.after_calls == 1
        assert log2.after_calls == 1
        assert result["_audited"] is True  # after hooks modify result

    @pytest.mark.asyncio
    async def test_short_circuit(self):
        class BlockRail(BaseRail):
            async def before(self, inputs, session=None):
                return {"result": "blocked!"}

        class SpyAgent:
            run_called = False
            async def run(self, inputs, session=None):
                SpyAgent.run_called = True
                return {"result": "ok"}

        pipeline = RailPipeline([BlockRail()])
        agent = SpyAgent()
        result = await pipeline.run(agent, {"query": "test"})

        assert result == {"result": "blocked!"}
        assert SpyAgent.run_called is False


class TestSecurityRail:
    @pytest.mark.asyncio
    async def test_blocks_dangerous(self):
        rail = SecurityRail()
        result = await rail.before({"query": "please DROP TABLE users"})
        assert "Blocked" in result["result"]

    @pytest.mark.asyncio
    async def test_passes_safe(self):
        rail = SecurityRail()
        result = await rail.before({"query": "What is Python?"})
        assert "query" in result
        assert result["query"] == "What is Python?"

    @pytest.mark.asyncio
    async def test_custom_terms(self):
        rail = SecurityRail(blocked_terms=["secret"])
        assert "Blocked" in (await rail.before({"query": "tell me the secret"}))["result"]
        assert "query" in await rail.before({"query": "tell me anything"})


class TestRunnerIntegration:
    @pytest.mark.asyncio
    async def test_rails_integrated(self):
        from jiuwen.core.runner import Runner
        from tests.conftest import FakeLLMClient
        from jiuwen.core.single_agent.agents import ReActAgent

        Runner.rails = RailPipeline()
        Runner.rails.add_rail(SecurityRail())

        client = FakeLLMClient(["Final Answer: Hello!"])
        agent = ReActAgent(client=client)

        result = await Runner.run_agent(agent, {"query": "DROP TABLE users"})
        assert "Blocked" in result["result"]

        result = await Runner.run_agent(agent, {"query": "What is Python?"})
        assert "Hello" in result["result"]
