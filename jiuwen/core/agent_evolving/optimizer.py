# coding: utf-8
"""Optimizer — generates improved prompts based on failure analysis."""

from typing import Any

from jiuwen.core.foundation.llm import LLMClient

_OPTIMIZER_PROMPT = """You are an expert at improving AI agent prompts.

Given the current prompt and examples where the agent failed, write a better prompt.

Current prompt:
{current_prompt}

Failed examples:
{failures}

Rules for the new prompt:
1. Be clear and specific about what the agent should do
2. Include any missing context that would help
3. Keep it concise

Output ONLY the new prompt text (no explanation, no markdown formatting)."""


class Optimizer:
    """Generates improved prompts based on evaluation failures.

    Usage::

        optimizer = Optimizer(client)
        new_prompt = await optimizer.optimize(
            current_prompt="You are a helpful assistant.",
            failures=[
                {"case": Case(...), "actual": "wrong answer"},
            ],
        )
    """

    def __init__(self, client: LLMClient):
        self._client = client

    async def optimize(
        self,
        current_prompt: str,
        failures: list[dict[str, Any]],
    ) -> str:
        """Generate an improved prompt.

        Args:
            current_prompt: The agent's current system prompt.
            failures: List of failed evaluation results.

        Returns:
            A new, improved system prompt string.
        """
        if not failures:
            return current_prompt

        failure_text = "\n\n".join(
            f"Input: {f['case'].input}\nExpected: {f['case'].expected}\nGot: {f['actual']}"
            for f in failures[:5]  # limit to 5 examples
        )

        messages = [{
            "role": "user",
            "content": _OPTIMIZER_PROMPT.format(
                current_prompt=current_prompt,
                failures=failure_text,
            ),
        }]

        try:
            response = await self._client.chat(messages)
            return response.strip()
        except Exception:
            return current_prompt
