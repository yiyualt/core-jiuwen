# coding: utf-8
"""Tests for AutoHarnessOrchestrator, PipelineSpec, and ExperienceStore."""

import pytest
from tests.conftest import FakeLLMClient
from jiuwen.auto_harness.pipeline import StageSpec, PipelineSpec, default_pipeline
from jiuwen.auto_harness.orchestrator import AutoHarnessOrchestrator
from jiuwen.auto_harness.experience import ExperienceStore


class TestPipelineSpec:
    def test_default_pipeline(self):
        pipe = default_pipeline()
        assert pipe.name == "standard"
        assert len(pipe.stages) == 4
        assert pipe.stages[0].name == "assess"
        assert pipe.stages[-1].name == "verify"

    def test_custom_pipeline(self):
        pipe = PipelineSpec(name="custom", stages=[
            StageSpec("analyze", "Analyze code", "You analyze code."),
        ])
        assert len(pipe.stages) == 1


class TestExperienceStore:
    def test_record_and_recent(self):
        store = ExperienceStore()
        store.record("assess", "task1", {"result": "ok"})
        store.record("implement", "task2", {"result": "done"})
        assert len(store) == 2
        assert len(store.recent(stage="assess")) == 1

    def test_clear(self):
        store = ExperienceStore()
        store.record("x", "t", {"r": "y"})
        store.clear()
        assert len(store) == 0


class TestOrchestrator:
    @pytest.mark.asyncio
    async def test_runs_pipeline(self):
        client = FakeLLMClient([
            "Final Answer: Found 2 issues.",   # assess
            "Final Answer: Fix both issues.",  # plan
            "Final Answer: Changes made.",     # implement
            "Final Answer: All tests pass.",   # verify
        ])
        pipe = PipelineSpec(name="test", stages=[
            StageSpec("assess", "Analyze", "You analyze."),
            StageSpec("verify", "Verify", "You verify."),
        ])
        orchestrator = AutoHarnessOrchestrator(client, pipeline=pipe)
        result = await orchestrator.run("Test task")
        assert "results" in result
        assert "assess" in result["results"]
        assert "verify" in result["results"]
        assert len(orchestrator.experience) == 2
