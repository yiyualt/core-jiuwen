``jiuwen.auto_harness``
=========================

.. module:: jiuwen.auto_harness

StageSpec
---------

.. class:: StageSpec(name: str, description: str, system_prompt: str = "")

PipelineSpec
------------

.. class:: PipelineSpec(name: str, stages: list[StageSpec])

.. function:: default_pipeline() -> PipelineSpec

AutoHarnessOrchestrator
------------------------

.. class:: AutoHarnessOrchestrator(client: LLMClient, pipeline: PipelineSpec | None = None, experience: ExperienceStore | None = None)

   .. method:: async run(task: str) -> dict

ExperienceStore
---------------

.. class:: ExperienceStore

   .. method:: record(stage: str, task: str, result: dict) -> None
   .. method:: recent(stage: str | None = None, limit: int = 10) -> list[dict]
   .. method:: clear() -> None
