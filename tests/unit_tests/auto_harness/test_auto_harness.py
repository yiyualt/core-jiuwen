# coding: utf-8
"""Tests for auto_harness V3 — fix loop, experience, session pipeline, orchestrator."""

import os
import tempfile

import pytest
from tests.conftest import FakeLLMClient
from jiuwen.auto_harness.registry import StageRegistry, PipelineRegistry
from jiuwen.auto_harness.contexts import SessionContext
from jiuwen.auto_harness.stages import (
    StageResult, AssessStage, PlanStage, ImplementStage, VerifyStage,
)
from jiuwen.auto_harness.pipeline import StandardPipeline, ExtendedPipeline
from jiuwen.auto_harness.orchestrator import AutoHarnessOrchestrator
from jiuwen.auto_harness.fix_loop import FixLoopController, FixLoopResult
from jiuwen.auto_harness.experience import ExperienceStore


class TestRegistry:
    def test_stage_registry(self):
        r = StageRegistry()
        r.register("assess", AssessStage)
        assert r.get("assess") is AssessStage

    def test_pipeline_registry(self):
        r = PipelineRegistry()
        r.register("standard", StandardPipeline)
        assert r.get("standard") is StandardPipeline
        with pytest.raises(KeyError):
            r.require("nonexistent")


class TestSessionContext:
    def test_artifacts(self):
        ctx = SessionContext()
        ctx.put_artifact("key", "value")
        assert ctx.get_artifact("key") == "value"

    def test_clone(self):
        ctx = SessionContext()
        ctx.put_artifact("x", 1)
        cloned = ctx.clone()
        assert cloned.get_artifact("x") == 1
        cloned.put_artifact("y", 2)
        assert ctx.get_artifact("y") is None


class TestStages:
    @pytest.mark.asyncio
    async def test_assess(self):
        client = FakeLLMClient(["Final Answer: Found 3 issues."])
        stage = AssessStage(client)
        ctx = SessionContext()
        ctx.put_artifact("task", "review code")
        result = await stage.execute(ctx)
        assert result.status == "success"


class TestPipeline:
    @pytest.mark.asyncio
    async def test_standard(self):
        client = FakeLLMClient([
            "Final Answer: ok", "Final Answer: ok",
            "Final Answer: ok", "Final Answer: ok",
        ])
        pipeline = StandardPipeline(client)
        ctx = SessionContext()
        ctx.put_artifact("task", "test")
        results = [r async for r in pipeline.stream(ctx)]
        assert len(results) == 4

    @pytest.mark.asyncio
    async def test_extended(self):
        client = FakeLLMClient(["Final Answer: a"] * 5)
        pipeline = ExtendedPipeline(client)
        ctx = SessionContext()
        ctx.put_artifact("task", "test")
        results = [r async for r in pipeline.stream(ctx)]
        assert len(results) == 5


class TestFixLoopV2:
    @pytest.mark.asyncio
    async def test_phase1_pass(self):
        ctrl = FixLoopController(phase1_max_retries=3, phase2_max_retries=1)
        calls = 0

        async def verify():
            nonlocal calls
            calls += 1
            return FixLoopResult(success=(calls >= 1))

        async def fixer(errors):
            pass

        result = await ctrl.run(verify, fixer)
        assert result.success
        assert result.phase == 1

    @pytest.mark.asyncio
    async def test_exhausted(self):
        ctrl = FixLoopController(phase1_max_retries=2, phase2_max_retries=0)
        async def verify():
            return FixLoopResult(success=False, error_log=["test failure"])
        async def fixer(errors):
            pass
        result = await ctrl.run(verify, fixer)
        assert not result.success


class TestExperienceStoreV2:
    def test_persistence(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            store = ExperienceStore(path)
            store.record("assess", "task a", {"result": "ok"})
            store.record_failure("verify", "task b", "failed")
            store.record_insight("learnings", "pattern x", "use async for db")

            # Load fresh
            store2 = ExperienceStore(path)
            assert len(store2) == 3

            # Search
            results = store2.search("task")
            assert len(results) >= 1

            # Synthesize
            ctx = store2.synthesize(results)
            assert "task a" in ctx
        finally:
            os.unlink(path)

    def test_clear(self):
        store = ExperienceStore()
        store.record("x", "t", {"result": "y"})
        store.clear()
        assert len(store) == 0


class TestOrchestrator:
    @pytest.mark.asyncio
    async def test_run_standard(self):
        client = FakeLLMClient(["Final Answer: ok"] * 4)
        orch = AutoHarnessOrchestrator(client)
        result = await orch.run("test", pipeline_name="standard")
        assert result["pipeline"] == "standard"
        assert len(result["results"]) == 4

    @pytest.mark.asyncio
    async def test_run_meta_evolve(self):
        # Meta pipeline needs assess, plan, implement*N, verify*N, learnings
        client = FakeLLMClient([
            "Final Answer: assessment done",            # assess
            "Final Answer: 1. fix login 2. add tests",  # plan
            "Final Answer: implemented fix 1",           # task 0 implement
            "Final Answer: verified fix 1",              # task 0 verify
            "Final Answer: implemented fix 2",           # task 1 implement
            "Final Answer: verified fix 2",              # task 1 verify
            "Final Answer: session learnings extracted", # learnings
        ])
        orch = AutoHarnessOrchestrator(client)
        result = await orch.run("test", pipeline_name="meta_evolve")
        assert result["pipeline"] == "meta_evolve"
        assert len(result["results"]) >= 4  # assess, plan, 2 tasks, learnings

    def test_select_pipeline(self):
        orch = AutoHarnessOrchestrator(FakeLLMClient(["ok"]))
        assert orch.select_pipeline() == "standard"
        assert orch.select_pipeline("meta_evolve") == "meta_evolve"
