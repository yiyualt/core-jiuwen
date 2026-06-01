# coding: utf-8
"""Graph base classes — abstract definitions for graph construction.

Defines the Graph ABC (the builder interface) and ExecutableGraph
(the compiled runtime form).
"""

from abc import ABC, abstractmethod
from typing import (
    Self,
    Union,
    Any,
    AsyncIterator,
    Hashable,
    Callable,
    Awaitable,
    Sequence,
)

from jiuwen.core.graph.executable import Executable, Input, Output

# Router: a callable that maps state to one or more target node IDs
Router = Union[
    Callable[..., Union[Hashable, Sequence[Hashable]]],
    Callable[..., Awaitable[Union[Hashable, Sequence[Hashable]]]],
]


class ExecutableGraph(Executable[Input, Output]):
    """A compiled graph that can be invoked like any Executable.

    Wraps the internal Pregel engine behind the standard Executable interface.
    """

    async def invoke(self, inputs: Input, session: Any = None) -> Output:
        """Execute the compiled graph with the given inputs."""
        return await self._invoke(inputs, session)

    @abstractmethod
    async def _invoke(self, inputs: Input, session: Any = None) -> Output:
        """Internal invoke implementation."""
        ...

    async def stream(self, inputs: Input, session: Any = None) -> AsyncIterator[Output]:
        """Stream output from the compiled graph."""
        if False:
            yield

    async def collect(self, inputs: AsyncIterator[Input], session: Any = None) -> Output:
        """Collect streaming inputs through the graph."""
        raise NotImplementedError("CompiledGraph does not support collect")

    async def transform(self, inputs: AsyncIterator[Input], session: Any = None) -> AsyncIterator[Output]:
        """Transform streaming inputs through the graph."""
        raise NotImplementedError("CompiledGraph does not support transform")
        if False:
            yield


class Graph(ABC):
    """Abstract builder for constructing executable graphs.

    Provides a fluent API for building DAGs:
    - add_node: register executable nodes
    - add_edge: connect nodes
    - add_conditional_edges: branch based on router output
    - compile: produce an ExecutableGraph
    """

    @abstractmethod
    def start_node(self, node_id: str) -> Self:
        """Mark a node as the entry point of the graph."""
        ...

    @abstractmethod
    def end_node(self, node_id: str) -> Self:
        """Mark a node as an exit point of the graph."""
        ...

    @abstractmethod
    def add_node(self, node_id: str, node: Executable, *, wait_for_all: bool = False) -> Self:
        """Register a node in the graph."""
        ...

    @abstractmethod
    def add_edge(self, source_node_id: Union[str, list[str]], target_node_id: str) -> Self:
        """Add a directed edge from source to target."""
        ...

    @abstractmethod
    def add_conditional_edges(self, source_node_id: str, router: Router) -> Self:
        """Add conditional edges branching from source via router."""
        ...

    @abstractmethod
    def compile(self, session: Any = None, **kwargs) -> ExecutableGraph:
        """Compile the graph into an executable form."""
        ...

    @abstractmethod
    def get_nodes(self) -> dict:
        """Return all registered nodes."""
        ...
