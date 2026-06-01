# coding: utf-8
"""Tests for ReActAgent — the Reasoning + Acting agent."""

import pytest
from tests.conftest import FakeLLMClient
from jiuwen.core.foundation.tool import ToolCard
from jiuwen.core.single_agent.agents.react_agent import ReActAgent


@pytest.fixture
def search_tool():
    def search(query: str) -> str:
        return f"Results for: {query}"
    return ToolCard(name="search", description="Search the web", parameters={"properties": {"query": {"type": "string"}}}, func=search)


@pytest.fixture
def calc_tool():
    def calculate(expr: str) -> str:
        return str(eval(expr))
    return ToolCard(name="calculate", description="Evaluate math", parameters={"properties": {"expr": {"type": "string"}}}, func=calculate)


class TestReActAgent:
    @pytest.mark.asyncio
    async def test_direct_final_answer(self):
        client = FakeLLMClient(["Final Answer: The sky is blue because of Rayleigh scattering."])
        agent = ReActAgent(client=client)
        result = await agent.run({"query": "Why is the sky blue?"})
        assert result == {"result": "The sky is blue because of Rayleigh scattering."}

    @pytest.mark.asyncio
    async def test_one_tool_call_then_answer(self, search_tool):
        client = FakeLLMClient([
            "Thought: I need to search\nAction: search(query='weather in Paris')",
            "Thought: I have the data\nFinal Answer: It is sunny in Paris.",
        ])
        agent = ReActAgent(client=client, tools=[search_tool])
        result = await agent.run({"query": "What's the weather?"})
        assert result["result"] == "It is sunny in Paris."

    @pytest.mark.asyncio
    async def test_multiple_tools(self, search_tool, calc_tool):
        client = FakeLLMClient([
            "Thought: Let me calculate\nAction: calculate(expr='2+2')",
            "Thought: Now search\nAction: search(query='meaning of life')",
            "Thought: I know\nFinal Answer: 42",
        ])
        agent = ReActAgent(client=client, tools=[search_tool, calc_tool])
        result = await agent.run({"query": "Complex question"})
        assert result["result"] == "42"

    @pytest.mark.asyncio
    async def test_max_iterations(self):
        # Agent that never gives final answer
        client = FakeLLMClient(["Action: search(query='x')"] * 20)
        agent = ReActAgent(client=client, max_iterations=3)
        result = await agent.run({"query": "test"})
        assert "Max iterations" in result["result"]

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        client = FakeLLMClient([
            "Action: nonexistent(x=1)",
            "Thought: that failed\nFinal Answer: I cannot help.",
        ])
        agent = ReActAgent(client=client)
        result = await agent.run({"query": "test"})
        assert result["result"] == "I cannot help."

    @pytest.mark.asyncio
    async def test_unknown_format_self_corrects(self):
        client = FakeLLMClient([
            "Just some random text without proper format",
            "Final Answer: Corrected.",
        ])
        agent = ReActAgent(client=client)
        result = await agent.run({"query": "test"})
        assert result["result"] == "Corrected."

    @pytest.mark.asyncio
    async def test_system_prompt_included(self):
        client = FakeLLMClient(["Final Answer: done"])
        agent = ReActAgent(client=client, system_prompt="You are a math tutor.")
        result = await agent.run({"query": "2+2"})
        assert result["result"] == "done"
        # Verify system prompt was included
        assert "math tutor" in client.last_messages[0]["content"]

    def test_parse_tool_call(self):
        name, args = ReActAgent._parse_tool_call("search(query='hello')")
        assert name == "search"
        assert args == {"query": "hello"}

    def test_parse_tool_call_multiple_args(self):
        name, args = ReActAgent._parse_tool_call("calc(a=1, b=2, op='add')")
        assert name == "calc"
        assert args == {"a": 1, "b": 2, "op": "add"}

    def test_parse_output_final(self):
        result = ReActAgent(client=None)._parse_output("Thought: I know\nFinal Answer: 42")
        assert result == {"type": "final", "answer": "42"}

    def test_parse_output_action(self):
        result = ReActAgent(client=None)._parse_output("Thought: let me check\nAction: search(q='x')")
        assert result == {"type": "action", "action": "search(q='x')"}

    def test_parse_output_unknown(self):
        result = ReActAgent(client=None)._parse_output("random gibberish")
        assert result["type"] == "unknown"
