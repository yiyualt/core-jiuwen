# coding: utf-8
"""AutoHarnessOrchestrator — runs optimization pipelines."""

from typing import Any

from jiuwen.core.foundation.llm import LLMClient
from jiuwen.core.single_agent.agents import ReActAgent
from jiuwen.auto_harness.pipeline import PipelineSpec, default_pipeline
from jiuwen.auto_harness.experience import ExperienceStore


class AutoHarnessOrchestrator:
    """Runs multi-stage optimization pipelines using specialized agents.

    Each stage uses a ReActAgent with a stage-specific system prompt
    to perform its part of the optimization.

    Usage::

        client = OpenAIClient.from_env()
        orchestrator = AutoHarnessOrchestrator(client)
        result = await orchestrator.run("Optimize the database module")
    """

    def __init__(
        self,
        client: LLMClient,
        pipeline: PipelineSpec | None = None,
        experience: ExperienceStore | None = None,
    ):
        self._client = client
        self._pipeline = pipeline or default_pipeline()
        self._experience = experience or ExperienceStore()

    @property
    def pipeline(self) -> PipelineSpec:
        return self._pipeline

    @property
    def experience(self) -> ExperienceStore:
        return self._experience

    async def run(self, task: str) -> dict[str, Any]:
        """Execute all stages of the pipeline on a task.

        Args:
            task: The optimization task description.

        Returns:
            Dict with per-stage results and accumulated experience.
        """
        results: dict[str, Any] = {}
        context = task

        for stage in self._pipeline.stages:
            agent = self._create_agent_for_stage(stage)
            result = await agent.run({"query": context})

            results[stage.name] = result
            self._experience.record(stage.name, task, result)

            # Pass result as context to next stage
            context = f"Previous stage ({stage.name}) result:\n{result.get('result', '')}\n\nOriginal task: {task}"

        return {"pipeline": self._pipeline.name, "results": results}

    def _create_agent_for_stage(self, stage) -> ReActAgent:
        return ReActAgent(
            client=self._client,
            system_prompt=stage.system_prompt,
        )
