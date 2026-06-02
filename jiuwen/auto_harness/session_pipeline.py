# coding: utf-8
"""MetaEvolvePipeline — session-level pipeline with per-task feedback loops."""

from typing import AsyncIterator

from jiuwen.core.foundation.llm import LLMClient
from jiuwen.auto_harness.contexts import SessionContext
from jiuwen.auto_harness.experience import ExperienceStore
from jiuwen.auto_harness.fix_loop import FixLoopController
from jiuwen.auto_harness.learnings_stage import LearningsStage
from jiuwen.auto_harness.pipeline import StandardPipeline, BasePipeline
from jiuwen.auto_harness.stages import (
    StageResult,
    AssessStage,
    PlanStage,
    ImplementStage,
    VerifyStage,
)


class MetaEvolvePipeline(BasePipeline):
    """Session-level pipeline: assess → plan → per-task loop → learnings.

    The "meta" pipeline that orchestrates multiple tasks within a session.
    Each task runs through implement → verify (with fix loop), and failures
    are recorded as experience for future sessions.
    """

    name = "meta_evolve"
    description = "Full session pipeline with per-task feedback loops"

    def __init__(self, client: LLMClient, experience: ExperienceStore,
                 fix_loop: FixLoopController | None = None):
        super().__init__(fix_loop)
        self._client = client
        self._experience = experience
        self._fix_loop = fix_loop or FixLoopController()

    async def stream(self, ctx: SessionContext) -> AsyncIterator[StageResult]:
        # Phase 1: Assess
        assess = AssessStage(self._client)
        assess_result = await assess.execute(ctx)
        ctx.put_artifact("assess", assess_result)
        yield assess_result

        # Phase 2: Plan
        plan = PlanStage(self._client)
        plan_result = await plan.execute(ctx)
        ctx.put_artifact("plan", plan_result)
        yield plan_result

        # Phase 3: For each task in the plan, run implement → verify
        # The plan output contains task descriptions. We simulate per-task execution.
        tasks_text = plan_result.output
        tasks = self._parse_tasks(tasks_text)

        task_results = []
        for i, task_desc in enumerate(tasks[:5]):  # cap at 5 tasks
            task_ctx = ctx.clone()
            task_ctx.put_artifact("task", task_desc)

            # Inject related experiences
            related = self._experience.search(task_desc, top_k=5)
            if related:
                exp_context = self._experience.synthesize(related)
                task_ctx.put_artifact("_experiences", exp_context)

            # Implement
            impl = ImplementStage(self._client)
            impl_result = await impl.execute(task_ctx)
            task_ctx.put_artifact("implement", impl_result)
            yield StageResult(stage_name=f"task_{i}_implement", status=impl_result.status,
                            output=impl_result.output)

            # Verify with fix loop
            verify = VerifyStage(self._client)
            verify_result = await verify.execute(task_ctx)
            task_ctx.put_artifact("verify", verify_result)

            if verify_result.status == "failed":
                self._experience.record_failure(
                    "verify", task_desc, verify_result.output
                )
                yield StageResult(stage_name=f"task_{i}_verify", status="failed",
                                output=f"REVERTED: {verify_result.output[:200]}")
            else:
                self._experience.record(
                    "verify", task_desc, {"result": verify_result.output},
                    exp_type=ExperienceStore.SUCCESS
                )
                yield StageResult(stage_name=f"task_{i}_verify", status="success",
                                output=verify_result.output)

            task_results.append({"task": task_desc, "status": verify_result.status})

        ctx.put_artifact("task_results", task_results)

        # Phase 4: Learnings
        learnings = LearningsStage(self._client, self._experience)
        learnings_result = await learnings.execute(ctx)
        yield learnings_result

    @staticmethod
    def _parse_tasks(plan_text: str) -> list[str]:
        """Extract task descriptions from plan output."""
        tasks = []
        for line in plan_text.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("- ")):
                tasks.append(line.lstrip("0123456789.-) "))
        if not tasks:
            tasks = [plan_text[:200]]  # fallback: whole plan as one task
        return tasks
