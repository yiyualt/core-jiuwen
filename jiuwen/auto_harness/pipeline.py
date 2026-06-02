# coding: utf-8
"""BasePipeline and standard pipeline implementations."""

from abc import ABC
from typing import AsyncIterator

from jiuwen.core.foundation.llm import LLMClient
from jiuwen.auto_harness.contexts import SessionContext
from jiuwen.auto_harness.stages import (
    BaseStage,
    StageResult,
    AssessStage,
    PlanStage,
    ImplementStage,
    VerifyStage,
)
from jiuwen.auto_harness.fix_loop import FixLoopController, FixLoopExecutor


class BasePipeline(ABC):
    """Abstract base for pipeline implementations.

    Pipelines own a sequence of stages. The orchestrator calls
    stream() to execute them with streaming output.
    """

    name: str = ""
    description: str = ""
    stages: list[BaseStage] = []

    def __init__(self, fix_loop: FixLoopController | None = None,
                 fix_loop_executor: FixLoopExecutor | None = None):
        self._fix_loop = fix_loop or FixLoopController()
        self._fix_loop_executor = fix_loop_executor

    async def stream(self, ctx: SessionContext) -> AsyncIterator[StageResult]:
        """Execute all stages, yielding results as they complete."""
        for stage in self.stages:
            result = await stage.execute(ctx)
            if result.status == "failed":
                if self._fix_loop_executor:
                    fix_result = await self._fix_loop_executor.run()
                    if fix_result.success:
                        result = StageResult(
                            stage_name=stage.name,
                            status="success",
                            output=f"Fixed after {fix_result.attempts} attempt(s). {fix_result.output}",
                            messages=[f"Fix loop succeeded in {fix_result.attempts} attempt(s)"],
                        )
                    else:
                        result = StageResult(
                            stage_name=stage.name,
                            status="failed",
                            output=f"Fix loop exhausted. {fix_result.output}",
                            messages=[f"Fix loop exhausted after {fix_result.attempts} attempts"],
                        )
                else:
                    result = await self._fix_loop.handle_failure(stage, ctx, result)
            ctx.put_artifact(stage.name, result)
            for msg in result.messages:
                ctx.add_message(msg)
            yield result


class StandardPipeline(BasePipeline):
    """Standard 4-stage pipeline: assess → plan → implement → verify."""

    name = "standard"
    description = "Standard optimization pipeline"

    def __init__(self, client: LLMClient, fix_loop: FixLoopController | None = None,
                 fix_loop_executor: FixLoopExecutor | None = None):
        super().__init__(fix_loop, fix_loop_executor=fix_loop_executor)
        self.stages = [
            AssessStage(client),
            PlanStage(client),
            ImplementStage(client),
            VerifyStage(client),
        ]


class ExtendedPipeline(BasePipeline):
    """Extended pipeline with two assessment rounds before planning."""

    name = "extended"
    description = "Extended pipeline with deeper analysis"

    def __init__(self, client: LLMClient, fix_loop: FixLoopController | None = None,
                 fix_loop_executor: FixLoopExecutor | None = None):
        super().__init__(fix_loop, fix_loop_executor=fix_loop_executor)
        self.stages = [
            AssessStage(client),
            AssessStage(client),
            PlanStage(client),
            ImplementStage(client),
            VerifyStage(client),
        ]
