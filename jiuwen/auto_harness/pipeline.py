# coding: utf-8
"""PipelineSpec — defines a sequence of optimization stages."""

from dataclasses import dataclass, field


@dataclass
class StageSpec:
    """A single stage in an optimization pipeline.

    Attributes:
        name: Stage identifier.
        description: What this stage does.
        system_prompt: System prompt for the agent in this stage.
    """

    name: str
    description: str
    system_prompt: str = ""


@dataclass
class PipelineSpec:
    """A complete optimization pipeline.

    Attributes:
        name: Pipeline identifier.
        stages: Ordered list of stages to execute.
    """

    name: str
    stages: list[StageSpec] = field(default_factory=list)


def default_pipeline() -> PipelineSpec:
    """Return the standard optimization pipeline."""
    return PipelineSpec(
        name="standard",
        stages=[
            StageSpec(
                "assess",
                "Analyze the current state and identify issues",
                "You are a code reviewer. Analyze the given code and identify issues.",
            ),
            StageSpec(
                "plan",
                "Create an improvement plan",
                "You are a planner. Based on the assessment, create a step-by-step improvement plan.",
            ),
            StageSpec(
                "implement",
                "Implement the planned changes",
                "You are a developer. Implement the changes described in the plan.",
            ),
            StageSpec(
                "verify",
                "Verify the changes work correctly",
                "You are a tester. Verify that the implemented changes work as expected.",
            ),
        ],
    )
