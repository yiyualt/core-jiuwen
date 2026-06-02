# coding: utf-8
"""Pipeline and Stage registries for auto-harness."""

from typing import Type


class StageRegistry:
    """Registry of available stages, keyed by name."""

    def __init__(self):
        self._stages: dict[str, Type] = {}

    def register(self, name: str, stage_cls: Type) -> None:
        self._stages[name] = stage_cls

    def get(self, name: str) -> Type | None:
        return self._stages.get(name)

    def names(self) -> list[str]:
        return list(self._stages.keys())


class PipelineRegistry:
    """Registry of available pipelines, keyed by name."""

    def __init__(self):
        self._pipelines: dict[str, Type] = {}

    def register(self, name: str, pipeline_cls: Type) -> None:
        self._pipelines[name] = pipeline_cls

    def get(self, name: str) -> Type | None:
        return self._pipelines.get(name)

    def names(self) -> list[str]:
        return list(self._pipelines.keys())

    def require(self, name: str) -> Type:
        cls = self._pipelines.get(name)
        if cls is None:
            raise KeyError(f"Pipeline '{name}' not found. Available: {self.names()}")
        return cls
