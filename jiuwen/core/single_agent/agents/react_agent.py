# coding: utf-8
"""ReActAgent — an agent that follows the Reasoning + Acting paradigm.

The agent loops: Thought → Action → Observation → repeat, until
it produces a Final Answer. Tools are discovered automatically
from the provided ToolCard list.
"""

import re
import ast
from typing import Any

from jiuwen.core.foundation.llm import LLMClient, ModelRequestConfig
from jiuwen.core.foundation.tool import ToolCard, ToolComponent

_REACT_SYSTEM_TEMPLATE = """You are {system_prompt}

You have access to the following tools:
{tool_descriptions}

Use the following format:

Thought: your reasoning about what to do next
Action: tool_name(param1=value1, param2=value2)
Observation: the result of the action
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the user's question

Rules:
- Always start with a Thought
- Use exactly one Action per step
- Use valid Python literal syntax for argument values
- When you have the answer, output Final Answer

{user_query}"""


class ReActAgent:
    """An AI agent that uses the ReAct (Reasoning + Acting) paradigm.

    The agent receives a set of tools and an LLM client. On each run,
    it enters a loop: think → choose tool → observe result → repeat,
    until it reaches a final answer.

    Usage::

        from jiuwen.core.single_agent.agents import ReActAgent
        from jiuwen.core.foundation import OpenAIClient, ToolCard

        client = OpenAIClient.from_env()

        def search(query: str) -> str:
            return f"Results for: {query}"

        agent = ReActAgent(
            client=client,
            tools=[ToolCard(name="search", func=search, ...)],
            system_prompt="You are a helpful research assistant.",
        )
        result = await agent.run({"query": "What is AI?"})
    """

    def __init__(
        self,
        client: LLMClient,
        tools: list[ToolCard] | None = None,
        system_prompt: str = "",
        max_iterations: int = 10,
    ):
        """Initialize the ReAct agent.

        Args:
            client: LLM client for reasoning.
            tools: List of ToolCards available to the agent.
            system_prompt: System-level instructions (role, context, etc.).
            max_iterations: Maximum number of Thought→Action cycles.
        """
        self._client = client
        self._tools: dict[str, ToolCard] = {}
        for tool in (tools or []):
            self._tools[tool.name] = tool
        self._system_prompt = system_prompt
        self._max_iterations = max_iterations

    async def run(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Execute the ReAct loop with the given inputs.

        Args:
            inputs: Must contain a "query" key with the user's question.

        Returns:
            Dict with "result" key containing the final answer.
        """
        query = inputs.get("query", "")
        messages = self._build_initial_messages(query)

        for _ in range(self._max_iterations):
            response = await self._client.chat(messages)
            parsed = self._parse_output(response)

            if parsed["type"] == "final":
                return {"result": parsed["answer"]}

            if parsed["type"] == "action":
                observation = await self._execute_action(parsed["action"])
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                # Unknown format — push the response and hope LLM self-corrects
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": "Continue. Use the required format."})

        return {"result": "Max iterations reached without final answer."}

    def _build_initial_messages(self, query: str) -> list[dict]:
        tool_descs = "\n".join(
            f"- {name}: {card.description}"
            + (f" (params: {', '.join(f'{k}: {v}' for k, v in card.parameters.get('properties', {}).items())})"
               if card.parameters else "")
            for name, card in self._tools.items()
        )

        system_msg = _REACT_SYSTEM_TEMPLATE.format(
            system_prompt=self._system_prompt or "a helpful AI assistant",
            tool_descriptions=tool_descs or "(no tools available)",
            user_query=f"User's question: {query}",
        )

        return [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": query},
        ]

    def _parse_output(self, text: str) -> dict:
        """Parse LLM output into a structured dict."""
        # Check for Final Answer
        if "Final Answer:" in text:
            answer = text.split("Final Answer:")[-1].strip()
            return {"type": "final", "answer": answer}

        # Check for Action
        action_match = re.search(r"Action:\s*(.+)", text)
        if action_match:
            action_str = action_match.group(1).strip()
            return {"type": "action", "action": action_str}

        # Unknown format
        return {"type": "unknown", "text": text}

    async def _execute_action(self, action_str: str) -> str:
        """Parse an action string and execute the corresponding tool."""
        tool_name, args = self._parse_tool_call(action_str)
        if tool_name not in self._tools:
            return f"Error: tool '{tool_name}' not found. Available: {list(self._tools.keys())}"

        tool = self._tools[tool_name]
        comp = ToolComponent(tool)
        try:
            result = await comp.invoke(args)
            return str(result.get("output", result))
        except Exception as e:
            return f"Error executing tool '{tool_name}': {e}"

    @staticmethod
    def _parse_tool_call(action_str: str) -> tuple[str, dict]:
        """Parse 'tool_name(k1=v1, k2=v2)' into (name, kwargs)."""
        match = re.match(r"(\w+)\((.*)\)", action_str.strip())
        if not match:
            raise ValueError(f"Cannot parse action: {action_str}")

        tool_name = match.group(1)
        args_str = match.group(2)

        kwargs = {}
        if args_str.strip():
            # Parse key=value pairs (quoted strings or non-comma/non-paren values)
            for pair in re.findall(r"(\w+)\s*=\s*(['\"].*?['\"]|[^,)]+)", args_str):
                key = pair[0]
                value = pair[1].strip()
                if value.startswith("'") or value.startswith('"'):
                    value = value[1:-1]
                else:
                    try:
                        value = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        pass
                kwargs[key] = value

        return tool_name, kwargs
