# coding: utf-8
"""WorkflowComponent — the base class for all workflow components."""

from abc import ABC
from typing import AsyncIterator

from jiuwen.core.graph.executable import Executable, Input, Output


class ComponentExecutable(Executable):
    """Base class for executable components.

    Delegates Executable's on_* methods to simpler invoke/stream/collect/transform.
    """

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        """Execute with batch input and return batch output. Override in subclasses."""
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement invoke(). "
            f"Override: async def invoke(self, inputs: dict, **kwargs) -> dict"
        )

    async def stream(self, inputs: dict, **kwargs) -> AsyncIterator[dict]:
        """Execute with batch input and yield streaming output."""
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement stream(). "
        )
        if False:
            yield {}

    async def collect(self, inputs: AsyncIterator[dict], **kwargs) -> dict:
        """Collect streaming input and return batch output."""
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement collect(). "
        )

    async def transform(self, inputs: AsyncIterator[dict], **kwargs) -> AsyncIterator[dict]:
        """Transform streaming input to streaming output."""
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement transform(). "
        )
        if False:
            yield {}

    # Delegate Executable's on_* to our invoke/stream/collect/transform
    async def on_invoke(self, inputs: Input, **kwargs) -> Output:
        return await self.invoke(inputs, **kwargs)

    async def on_stream(self, inputs: Input, **kwargs) -> AsyncIterator[Output]:
        async for chunk in self.stream(inputs, **kwargs):
            yield chunk

    async def on_collect(self, inputs: Input, **kwargs) -> Output:
        return await self.collect(inputs, **kwargs)

    async def on_transform(self, inputs: Input, **kwargs) -> AsyncIterator[Output]:
        async for chunk in self.transform(inputs, **kwargs):
            yield chunk


class ComponentComposable(ABC):
    """Mixin for components that can be added to a workflow graph."""

    def to_executable(self) -> Executable:
        if isinstance(self, Executable):
            return self
        class_name = type(self).__name__
        raise NotImplementedError(f"Component '{class_name}' does not implement to_executable().")


class WorkflowComponent(ComponentExecutable, ComponentComposable):
    """Standard component combining execution and graph construction.

    This is the primary base class for user-defined workflow components.
    Override invoke() for the most common batch-in/batch-out pattern.
    """

    def to_executable(self) -> Executable:
        return self
