# coding: utf-8
"""Team and CoordinatorAgent — multi-agent orchestration.

A Team bundles specialized agents under a Coordinator that
delegates subtasks to the right member.
"""

import asyncio
from typing import Any

from jiuwen.core.foundation.llm import LLMClient
from jiuwen.core.foundation.tool import ToolCard
from jiuwen.core.single_agent.agents.react_agent import ReActAgent

_COORDINATOR_SYSTEM_PROMPT = """You are a team coordinator. You have access to team members via the delegate tool.

Your job:
1. Analyze the user's request
2. Break it into subtasks
3. Delegate each subtask to the appropriate team member
4. Synthesize results into a final answer

Available team members:
{member_descriptions}

When delegating, specify:
- agent_name: which team member to use
- task: what to ask them to do

After gathering all needed information, provide a Final Answer that synthesizes the results."""


class CoordinatorAgent(ReActAgent):
    """A ReActAgent with built-in delegation to team members.

    The coordinator breaks complex tasks into subtasks and delegates
    each to the most appropriate member agent.

    Usage::

        members = {
            "researcher": ReActAgent(client, tools=[search]),
            "writer": ReActAgent(client, tools=[]),
        }
        coordinator = CoordinatorAgent(client=client, members=members)
        result = await coordinator.run({"query": "Research and write about AI"})
    """

    def __init__(
        self,
        client: LLMClient,
        members: dict[str, Any] | None = None,
        system_prompt: str = "",
        max_iterations: int = 10,
    ):
        """Initialize the coordinator.

        Args:
            client: LLM client for reasoning.
            members: Dict of {name: agent} for team members.
            system_prompt: Additional system instructions.
            max_iterations: Max delegation rounds.
        """
        self._members = members or {}
        self._member_descriptions = self._build_member_descriptions()

        # Build the delegate tool
        async def delegate(agent_name: str, task: str) -> str:
            member = self._members.get(agent_name)
            if not member:
                return f"Error: no member named '{agent_name}'. Available: {list(self._members.keys())}"
            try:
                result = await member.run({"query": task})
                return str(result.get("result", result))
            except Exception as e:
                return f"Error delegating to '{agent_name}': {e}"

        delegate_tool = ToolCard(
            name="delegate",
            description="Delegate a task to a team member",
            parameters={
                "type": "object",
                "properties": {
                    "agent_name": {"type": "string", "description": "Name of the team member"},
                    "task": {"type": "string", "description": "Task to delegate"},
                },
                "required": ["agent_name", "task"],
            },
            func=delegate,
        )

        full_prompt = _COORDINATOR_SYSTEM_PROMPT.format(
            member_descriptions=self._member_descriptions
        )
        if system_prompt:
            full_prompt = system_prompt + "\n\n" + full_prompt

        super().__init__(
            client=client,
            tools=[delegate_tool],
            system_prompt=full_prompt,
            max_iterations=max_iterations,
        )

    def _build_member_descriptions(self) -> str:
        lines = []
        for name, agent in self._members.items():
            desc = f"- **{name}**"
            if hasattr(agent, '_system_prompt') and agent._system_prompt:
                desc += f": {agent._system_prompt[:100]}"
            lines.append(desc)
        return "\n".join(lines) if lines else "(no members)"


class Team:
    """A team of specialized agents coordinated by a leader.

    Usage::

        researcher = ReActAgent(client, tools=[search_tool])
        writer = ReActAgent(client, tools=[])

        team = Team(
            members={"researcher": researcher, "writer": writer},
            client=client,
        )
        result = await team.run("Research AI safety and write a report")
    """

    def __init__(
        self,
        members: dict[str, Any],
        client: LLMClient | None = None,
        system_prompt: str = "",
    ):
        """Initialize the team.

        Args:
            members: Dict of {name: agent} for team members.
            client: LLM client for the coordinator. If None, uses OpenAIClient.from_env().
            system_prompt: Optional custom system prompt for the coordinator.
        """
        self._members = members

        if client is None:
            from jiuwen.core.foundation.llm import OpenAIClient
            client = OpenAIClient.from_env()

        self._coordinator = CoordinatorAgent(
            client=client,
            members=members,
            system_prompt=system_prompt,
        )

    @property
    def members(self) -> dict:
        return dict(self._members)

    async def run(self, task: str) -> dict[str, Any]:
        """Execute a complex task through the team.

        Args:
            task: The task description for the coordinator.

        Returns:
            Dict with "result" key containing the final answer.
        """
        return await self._coordinator.run({"query": task})
