# coding: utf-8
"""Executable base class — the fundamental unit of computation in the graph.

Every node in a workflow graph is an Executable. It supports four I/O modes:
- invoke: batch input → batch output
- stream: batch input → streaming output
- collect: streaming input → batch output
- transform: streaming input → streaming output
"""

from typing import TypeVar, Generic, AsyncIterator, Any

Input = TypeVar("Input", contravariant=True)
Output = TypeVar("Output", covariant=True)


class Executable(Generic[Input, Output]):
    """Base class for all invokable components in the graph.

    Subclasses override the on_* methods to provide specific behavior.
    The default implementations raise NotImplementedError with
    descriptive messages.
    """

    async def on_invoke(self, inputs: Input, **kwargs) -> Output:
        """Execute with batch input and return batch output.

        This is the primary execution mode for most components.
        """
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement on_invoke. "
            f"Override this method to provide inference logic."
        )

    async def on_stream(self, inputs: Input, **kwargs) -> AsyncIterator[Output]:
        """Execute with batch input and yield streaming output."""
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement on_stream. "
            f"Override this method to provide streaming logic."
        )

    async def on_collect(self, inputs: AsyncIterator[Input], **kwargs) -> Output:
        """Collect streaming input and return batch output."""
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement on_collect. "
            f"Override this method to provide collection logic."
        )

    async def on_transform(self, inputs: AsyncIterator[Input], **kwargs) -> AsyncIterator[Output]:
        """Transform streaming input to streaming output."""
        class_name = type(self).__name__
        raise NotImplementedError(
            f"Component '{class_name}' does not implement on_transform. "
            f"Override this method to provide transformation logic."
        )

    def skip_trace(self) -> bool:
        """Whether to skip tracing for this component."""
        return False

    def graph_invoker(self) -> bool:
        """Whether this component invokes a subgraph."""
        return False

    def post_commit(self) -> bool:
        """Whether to commit after execution."""
        return True

    def component_type(self) -> str:
        """Return the component type string."""
        return ""


GeneralExecutor = Executable[dict[str, Any], dict[str, Any]]
