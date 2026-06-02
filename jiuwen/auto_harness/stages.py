# coding: utf-8
"""BaseStage and built-in pipeline stages."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from jiuwen.core.foundation.llm import LLMClient
from jiuwen.core.single_agent.agents import ReActAgent
from jiuwen.auto_harness.contexts import SessionContext


@dataclass
class StageResult:
    """Result of executing a single pipeline stage.

    Attributes:
        stage_name: Name of the stage.
        status: "success" or "failed".
        output: Text output from the stage.
        artifacts: Dict of artifacts produced by this stage.
        messages: Human-readable messages.
    """

    stage_name: str
    status: str = "success"
    output: str = ""
    artifacts: dict[str, Any] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)


class BaseStage(ABC):
    """Abstract base for a pipeline stage.

    Subclasses implement execute() to perform the stage's work.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    async def execute(self, ctx: SessionContext) -> StageResult:
        """Execute this stage.

        Args:
            ctx: Session context with artifacts from previous stages.

        Returns:
            StageResult indicating success or failure.
        """
        ...


class AssessStage(BaseStage):
    """Analyzes the current state and identifies issues."""

    name = "assess"
    description = "Analyze code and identify issues"

    def __init__(self, client: LLMClient):
        self._client = client

    async def execute(self, ctx: SessionContext) -> StageResult:
        task = ctx.get_artifact("task", "analyze the code")
        agent = ReActAgent(
            client=self._client,
            system_prompt="You are a code reviewer. Analyze the given code and identify issues, bugs, and improvements.",
        )
        result = await agent.run({"query": task})
        output = str(result.get("result", ""))
        return StageResult(
            stage_name=self.name,
            status="success",
            output=output,
            messages=[f"Assessment: {output[:200]}..."],
        )


class PlanStage(BaseStage):
    """Creates an improvement plan based on assessment."""

    name = "plan"
    description = "Create an improvement plan"

    def __init__(self, client: LLMClient):
        self._client = client

    async def execute(self, ctx: SessionContext) -> StageResult:
        assessment = ctx.get_artifact("assess", StageResult(stage_name="assess", output=""))
        task = ctx.get_artifact("task", "")
        agent = ReActAgent(
            client=self._client,
            system_prompt="You are a planner. Based on the assessment, create a step-by-step improvement plan.",
        )
        result = await agent.run({
            "query": f"Assessment:\n{assessment.output}\n\nOriginal task: {task}\n\nCreate a plan."
        })
        output = str(result.get("result", ""))
        return StageResult(
            stage_name=self.name,
            status="success",
            output=output,
            messages=[f"Plan: {output[:200]}..."],
        )


class ImplementStage(BaseStage):
    """Implements the planned changes."""

    name = "implement"
    description = "Implement the changes"

    def __init__(self, client: LLMClient):
        self._client = client

    async def execute(self, ctx: SessionContext) -> StageResult:
        plan = ctx.get_artifact("plan", StageResult(stage_name="plan", output=""))
        agent = ReActAgent(
            client=self._client,
            system_prompt="You are a developer. Implement the changes described in the plan.",
        )
        result = await agent.run({
            "query": f"Plan:\n{plan.output}\n\nImplement the changes."
        })
        output = str(result.get("result", ""))
        return StageResult(
            stage_name=self.name,
            status="success",
            output=output,
            messages=[f"Implementation: {output[:200]}..."],
        )


class VerifyStage(BaseStage):
    """Verifies that the changes work correctly."""

    name = "verify"
    description = "Verify the changes"

    def __init__(self, client: LLMClient):
        self._client = client

    async def execute(self, ctx: SessionContext) -> StageResult:
        implementation = ctx.get_artifact("implement", StageResult(stage_name="implement", output=""))
        agent = ReActAgent(
            client=self._client,
            system_prompt="You are a tester. Verify that the implemented changes work as expected.",
        )
        result = await agent.run({
            "query": f"Implementation:\n{implementation.output}\n\nVerify the changes work."
        })
        output = str(result.get("result", ""))
        return StageResult(
            stage_name=self.name,
            status="success",
            output=output,
            messages=[f"Verification: {output[:200]}..."],
        )
