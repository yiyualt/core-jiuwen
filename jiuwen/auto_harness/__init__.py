# coding: utf-8
"""Auto Harness — automated agent optimization framework.

Three feedback loops:
1. CI Fix Loop — agent fixes CI failures automatically
2. Intra-session experience injection — tasks learn from each other
3. Inter-session learning — experiences persist across runs
"""

from jiuwen.auto_harness.registry import StageRegistry, PipelineRegistry
from jiuwen.auto_harness.contexts import SessionContext
from jiuwen.auto_harness.stages import BaseStage, StageResult, AssessStage, PlanStage, ImplementStage, VerifyStage
from jiuwen.auto_harness.pipeline import BasePipeline, StandardPipeline, ExtendedPipeline
from jiuwen.auto_harness.session_pipeline import MetaEvolvePipeline
from jiuwen.auto_harness.learnings_stage import LearningsStage
from jiuwen.auto_harness.orchestrator import AutoHarnessOrchestrator
from jiuwen.auto_harness.experience import ExperienceStore
from jiuwen.auto_harness.fix_loop import (
    FixLoopController,
    FixLoopResult,
    CommandVerifier,
    AgentFixer,
    OutputEvaluator,
    FixLoopExecutor,
)

__all__ = [
    "StageRegistry", "PipelineRegistry",
    "SessionContext",
    "BaseStage", "StageResult", "AssessStage", "PlanStage", "ImplementStage", "VerifyStage",
    "BasePipeline", "StandardPipeline", "ExtendedPipeline",
    "MetaEvolvePipeline", "LearningsStage",
    "AutoHarnessOrchestrator",
    "ExperienceStore",
    "FixLoopController", "FixLoopResult",
    "CommandVerifier", "AgentFixer", "OutputEvaluator", "FixLoopExecutor",
]
