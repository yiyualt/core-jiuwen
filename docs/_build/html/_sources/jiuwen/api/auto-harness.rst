``jiuwen.auto_harness``
=========================

.. module:: jiuwen.auto_harness

Registry
--------

.. class:: StageRegistry

   .. method:: register(name: str, stage_cls: Type) -> None
   .. method:: get(name: str) -> Type | None
   .. method:: names() -> list[str]

.. class:: PipelineRegistry

   .. method:: register(name: str, pipeline_cls: Type) -> None
   .. method:: get(name: str) -> Type | None
   .. method:: names() -> list[str]
   .. method:: require(name: str) -> Type

SessionContext
--------------

.. class:: SessionContext(orchestrator=None)

   .. method:: put_artifact(key: str, value) -> None
   .. method:: get_artifact(key: str, default=None) -> Any
   .. method:: clone() -> SessionContext

Stages
------

.. class:: BaseStage

   .. attribute:: name: str
   .. attribute:: description: str
   .. method:: async execute(ctx: SessionContext) -> StageResult

.. class:: StageResult(stage_name: str, status: str = "success", output: str = "", artifacts: dict = {}, messages: list[str] = [])

.. class:: AssessStage(client: LLMClient)
.. class:: PlanStage(client: LLMClient)
.. class:: ImplementStage(client: LLMClient)
.. class:: VerifyStage(client: LLMClient)

Pipelines
---------

.. class:: BasePipeline

   .. attribute:: name: str
   .. attribute:: stages: list[BaseStage]
   .. method:: async stream(ctx: SessionContext) -> AsyncIterator[StageResult]

.. class:: StandardPipeline(client: LLMClient, fix_loop=None)
.. class:: ExtendedPipeline(client: LLMClient, fix_loop=None)
.. class:: MetaEvolvePipeline(client: LLMClient, experience: ExperienceStore, fix_loop=None)

   Session-level pipeline: assess → plan → per-task implement+verify (with fix loop) → learnings.

.. class:: LearningsStage(client: LLMClient, experience: ExperienceStore)

   Post-session reflection stage. Extracts structured learnings from session results.

Orchestrator
------------

.. class:: AutoHarnessOrchestrator(client=None, pipeline_registry=None, stage_registry=None, experience=None, fix_loop=None)

   .. method:: select_pipeline(name: str | None = None) -> str
   .. method:: async run(task: str, pipeline_name=None) -> dict
   .. method:: async run_stream(task: str, pipeline_name=None) -> AsyncIterator[StageResult]

Fix Loop
--------

.. class:: FixLoopResult(success: bool, attempts: int = 0, phase: int = 1, error_log: list[str] = [], output: str = "")

.. class:: FixLoopController(phase1_max_retries: int = 5, phase2_max_retries: int = 3)

   .. method:: async run(verify_fn, fix_fn=None, evaluator=None) -> FixLoopResult
   .. method:: should_retry(stage_name: str) -> bool
   .. method:: reset() -> None

Experience
----------

.. class:: ExperienceStore(file_path: str | None = None)

   .. attribute:: SUCCESS: str, FAILURE: str, INSIGHT: str

   .. method:: record(stage, task, result, exp_type=SUCCESS) -> None
   .. method:: record_failure(stage, task, error) -> None
   .. method:: record_insight(stage, topic, insight) -> None
   .. method:: search(query: str, top_k: int = 10) -> list[dict]
   .. method:: synthesize(experiences: list[dict], max_tokens: int = 2000) -> str
   .. method:: recent(stage=None, limit=10) -> list[dict]
   .. method:: clear() -> None
