# coding: utf-8
"""BaseRail and RailPipeline — composable middleware for agents.

Rails are before/after hooks that wrap agent execution.
Multiple rails compose into a pipeline.
"""

from abc import ABC
from typing import Any


class BaseRail(ABC):
    """Abstract base for agent middleware rails.

    Override before() and/or after() to add behavior around
    agent execution. Default implementations pass through unchanged.

    Usage::

        class LoggingRail(BaseRail):
            async def before(self, inputs, session=None):
                print(f"Agent called with: {inputs}")
                return inputs
            async def after(self, result, session=None):
                print(f"Agent returned: {result}")
                return result
    """

    async def before(self, inputs: dict[str, Any], session: Any = None) -> dict[str, Any]:
        """Called before agent.run(). Can modify or intercept inputs.

        Args:
            inputs: The input dict passed to the agent.
            session: Optional session for context.

        Returns:
            Inputs dict (possibly modified), or a result dict to
            short-circuit the agent entirely.
        """
        return inputs

    async def after(self, result: dict[str, Any], session: Any = None) -> dict[str, Any]:
        """Called after agent.run(). Can modify or audit results.

        Args:
            result: The result dict returned by the agent.
            session: Optional session for context.

        Returns:
            Result dict (possibly modified).
        """
        return result


class RailPipeline:
    """Orchestrates multiple rails around agent execution.

    Execution order:
        rail[0].before → rail[1].before → ... → agent.run → rail[N].after → rail[N-1].after → ...
    """

    def __init__(self, rails: list[BaseRail] | None = None):
        self._rails: list[BaseRail] = rails or []

    def add_rail(self, rail: BaseRail) -> None:
        """Append a rail to the pipeline."""
        self._rails.append(rail)

    @property
    def rails(self) -> list[BaseRail]:
        return list(self._rails)

    async def run(
        self,
        agent: Any,
        inputs: dict[str, Any],
        session: Any = None,
    ) -> dict[str, Any]:
        """Execute the full pipeline: before hooks → agent → after hooks.

        Args:
            agent: The agent to run (must have async run(inputs, session) method).
            inputs: Input data.
            session: Optional session.

        Returns:
            The result from the agent (possibly modified by after hooks).
        """
        # Before hooks (forward)
        for rail in self._rails:
            inputs = await rail.before(inputs, session)
            # If a rail returns a "result" key directly, it's short-circuiting
            if "result" in inputs and not isinstance(inputs.get("result"), dict):
                pass  # Continue through remaining rails

        # If any rail returned a final result, skip agent
        if set(inputs.keys()) == {"result"}:
            return inputs

        # Agent execution
        result = await agent.run(inputs, session=session)

        # After hooks (reverse)
        for rail in reversed(self._rails):
            result = await rail.after(result, session)

        return result
