# coding: utf-8
"""AutoHarnessOrchestrator — session controller and pipeline dispatcher."""

from typing import AsyncIterator

from jiuwen.core.foundation.llm import LLMClient, OpenAIClient
from jiuwen.auto_harness.contexts import SessionContext
from jiuwen.auto_harness.experience import ExperienceStore
from jiuwen.auto_harness.fix_loop import FixLoopController
from jiuwen.auto_harness.pipeline import StandardPipeline, ExtendedPipeline
from jiuwen.auto_harness.session_pipeline import MetaEvolvePipeline
from jiuwen.auto_harness.registry import PipelineRegistry, StageRegistry
from jiuwen.auto_harness.stages import StageResult


class AutoHarnessOrchestrator:
    """Session controller that selects and runs optimization pipelines.

    Usage::

        client = OpenAIClient.from_env()
        orch = AutoHarnessOrchestrator(client)

        # Sync: standard 4-stage pipeline
        result = await orch.run("Optimize auth module")

        # Session-level: full meta pipeline with fix loops + learnings
        result = await orch.run("Optimize project", pipeline_name="meta_evolve")

        # Streaming
        async for r in orch.run_stream("Optimize auth module"):
            print(f"[{r.stage_name}] {r.status}")
    """

    def __init__(
        self,
        client: LLMClient | None = None,
        pipeline_registry: PipelineRegistry | None = None,
        stage_registry: StageRegistry | None = None,
        experience: ExperienceStore | None = None,
        fix_loop: FixLoopController | None = None,
    ):
        self._client = client or OpenAIClient.from_env()
        self._pipeline_registry = pipeline_registry or PipelineRegistry()
        self._stage_registry = stage_registry or StageRegistry()
        self._experience = experience or ExperienceStore()
        self._fix_loop = fix_loop or FixLoopController()

        self._pipeline_registry.register("standard", StandardPipeline)
        self._pipeline_registry.register("extended", ExtendedPipeline)
        self._pipeline_registry.register("meta_evolve", MetaEvolvePipeline)

    @property
    def pipeline_registry(self) -> PipelineRegistry:
        return self._pipeline_registry

    @property
    def stage_registry(self) -> StageRegistry:
        return self._stage_registry

    @property
    def experience(self) -> ExperienceStore:
        return self._experience

    def select_pipeline(self, name: str | None = None) -> str:
        available = self._pipeline_registry.names()
        if not available:
            raise ValueError("No pipelines registered")
        if name and name in available:
            return name
        if "standard" in available:
            return "standard"
        return available[0]

    def _make_pipeline(self, pipeline_cls):
        """Instantiate a pipeline with appropriate arguments."""
        if pipeline_cls is MetaEvolvePipeline:
            return pipeline_cls(self._client, self._experience, self._fix_loop)
        return pipeline_cls(self._client, self._fix_loop)

    async def run(self, task: str, pipeline_name: str | None = None) -> dict:
        selected = self.select_pipeline(pipeline_name)
        pipeline_cls = self._pipeline_registry.require(selected)
        pipeline = self._make_pipeline(pipeline_cls)

        ctx = SessionContext(orchestrator=self)
        ctx.put_artifact("task", task)

        results = {}
        async for result in pipeline.stream(ctx):
            results[result.stage_name] = {"status": result.status, "output": result.output}

        return {"pipeline": selected, "results": results}

    async def run_stream(self, task: str, pipeline_name: str | None = None) -> AsyncIterator[StageResult]:
        selected = self.select_pipeline(pipeline_name)
        pipeline_cls = self._pipeline_registry.require(selected)
        pipeline = self._make_pipeline(pipeline_cls)

        ctx = SessionContext(orchestrator=self)
        ctx.put_artifact("task", task)

        async for result in pipeline.stream(ctx):
            self._experience.record(result.stage_name, task, {"result": result.output})
            yield result
