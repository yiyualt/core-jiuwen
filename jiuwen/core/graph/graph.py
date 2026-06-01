# coding: utf-8
"""PregelGraph — the concrete DAG construction and compilation engine.

Builds on the Pregel model: nodes communicate through channels,
execution proceeds in super-steps.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Hashable, Self, Sequence

from jiuwen.core.graph.base import Graph, Router, ExecutableGraph
from jiuwen.core.graph.executable import Executable, Output
from jiuwen.core.graph.channels import TriggerChannel, BarrierChannel, Channel

# Sentinel markers for graph boundaries
START = "__start__"
END = "__end__"
MAX_RECURSIVE_LIMIT = 100


@dataclass
class TriggerMessage:
    """Message that fires a trigger channel."""
    sender: str
    target: str


@dataclass
class BarrierMessage:
    """Message that contributes to a barrier channel."""
    sender: str
    target: str


@dataclass
class Branch:
    """A conditional branch with a router function."""
    condition: Callable[..., Hashable | Sequence[Hashable]]


class PregelGraph(Graph):
    """Concrete graph builder using the Pregel execution model."""

    def __init__(self):
        self.edges: list[tuple[str | list[str], str]] = []
        self.waits: set[str] = set()
        self.nodes: dict[str, Executable] = {}
        self.branches: dict[str, dict[str, Branch]] = {}
        self._start_nodes: list[str] = []
        self._end_nodes: set[str] = set()

    def start_node(self, node_id: str) -> Self:
        self._validate_node_id(node_id)
        self._start_nodes.append(node_id)
        return self

    def end_node(self, node_id: str) -> Self:
        self._validate_node_id(node_id)
        self._end_nodes.add(node_id)
        return self

    def add_node(self, node_id: str, node: Executable, *, wait_for_all: bool = False) -> Self:
        self._validate_node_id(node_id)
        if node is None:
            raise ValueError(f"Node '{node_id}' is None")
        if node_id in self.nodes:
            raise ValueError(f"Node '{node_id}' already exists")
        self.nodes[node_id] = node
        if wait_for_all:
            self.waits.add(node_id)
        return self

    def add_edge(self, source_node_id: str | list[str], target_node_id: str) -> Self:
        if not source_node_id:
            raise ValueError(f"Invalid edge: source='{source_node_id}', target='{target_node_id}'")
        if isinstance(source_node_id, list):
            for item in source_node_id:
                if not item:
                    raise ValueError(f"Invalid edge: source list contains empty value")
        if not target_node_id:
            raise ValueError(f"Invalid edge: source='{source_node_id}', target is empty")
        self.edges.append((source_node_id, target_node_id))
        return self

    def add_conditional_edges(self, source_node_id: str, router: Router) -> Self:
        if not source_node_id:
            raise ValueError(f"Invalid conditional edge: source is empty")
        if router is None:
            raise ValueError(f"Invalid conditional edge: router is None")
        name = _get_callable_name(router)
        if source_node_id not in self.branches:
            self.branches[source_node_id] = {}
        self.branches[source_node_id][name] = Branch(router)
        return self

    def get_nodes(self) -> dict:
        return dict(self.nodes)

    def compile(self, session: Any = None, **kwargs) -> ExecutableGraph:
        # Build adjacency: source → [targets]
        adjacency: dict[str, list[str]] = {}
        for source, target in self.edges:
            if isinstance(source, list):
                for s in source:
                    adjacency.setdefault(s, []).append(target)
            else:
                adjacency.setdefault(source, []).append(target)

        # Create channels
        channels: dict[str, Channel] = {}
        for source, target in self.edges:
            if target in self.waits:
                expected = set(source) if isinstance(source, list) else {source}
                key = _barrier_key(source, target)
                if key not in channels:
                    channels[key] = BarrierChannel(target, expected)
            else:
                ch_key = f"trigger:{target}"
                if ch_key not in channels:
                    channels[ch_key] = TriggerChannel(target)

        for start_id in self._start_nodes:
            ch_key = f"trigger:{start_id}"
            if ch_key not in channels:
                channels[ch_key] = TriggerChannel(start_id)

        for end_id in self._end_nodes:
            ch_key = f"trigger:{end_id}"
            if ch_key not in channels:
                channels[ch_key] = TriggerChannel(end_id)

        return CompiledGraph(
            nodes=dict(self.nodes),
            channels=channels,
            start_nodes=list(self._start_nodes),
            end_nodes=set(self._end_nodes),
            branches=dict(self.branches),
            adjacency=adjacency,
            waits=self.waits,
        )

    def _validate_node_id(self, node_id: str) -> None:
        if not node_id:
            raise ValueError("Node ID cannot be None or empty")


class CompiledGraph(ExecutableGraph):
    """A compiled PregelGraph ready for execution."""

    def __init__(
        self,
        nodes: dict[str, Executable],
        channels: dict[str, Channel],
        start_nodes: list[str],
        end_nodes: set[str],
        branches: dict[str, dict[str, Branch]],
        adjacency: dict[str, list[str]] | None = None,
        waits: set[str] | None = None,
    ):
        self._nodes = nodes
        self._channels = channels
        self._start_nodes = start_nodes
        self._end_nodes = end_nodes
        self._branches = branches
        self._adjacency = adjacency or {}
        self._waits = waits or set()
        self._node_outputs: dict[str, Any] = {}

    async def _invoke(self, inputs: dict, session: Any = None) -> Output:
        step = 0
        for start_id in self._start_nodes:
            self._seed_node(start_id)

        while step < MAX_RECURSIVE_LIMIT:
            ready = self._get_ready_nodes()
            if not ready:
                break
            tasks = [self._execute_node(node_id, inputs) for node_id in ready]
            await asyncio.gather(*tasks)
            step += 1

        result: dict[str, Any] = {}
        for end_id in self._end_nodes:
            if end_id in self._node_outputs:
                result[end_id] = self._node_outputs[end_id]
        return result

    def _seed_node(self, node_id: str) -> None:
        ch_key = f"trigger:{node_id}"
        ch = self._channels.get(ch_key)
        if ch is None:
            for key, channel in self._channels.items():
                if channel.node_name == node_id and key.startswith("barrier:"):
                    ch = channel
                    break
        if ch:
            ch.accept(TriggerMessage(sender=START, target=node_id))

    def _get_ready_nodes(self) -> list[str]:
        ready = []
        for ch in self._channels.values():
            node_id = ch.node_name
            if node_id in self._nodes and ch.is_ready() and node_id not in self._node_outputs:
                ready.append(node_id)
        return ready

    async def _execute_node(self, node_id: str, inputs: dict) -> None:
        node = self._nodes[node_id]
        for ch in self._channels.values():
            if ch.node_name == node_id and ch.is_ready():
                ch.consume()

        try:
            result = await node.on_invoke(inputs)
        except NotImplementedError:
            raise

        self._node_outputs[node_id] = result
        downstream = self._adjacency.get(node_id, [])
        for target_id in downstream:
            self._route_to_target(node_id, target_id)

    def _route_to_target(self, source_id: str, target_id: str) -> None:
        if target_id in self._waits:
            for key, ch in self._channels.items():
                if ch.node_name == target_id and key.startswith("barrier:"):
                    ch.accept(BarrierMessage(sender=source_id, target=target_id))
                    return
        else:
            ch_key = f"trigger:{target_id}"
            ch = self._channels.get(ch_key)
            if ch:
                ch.accept(TriggerMessage(sender=source_id, target=target_id))


def _get_callable_name(func) -> str:
    if hasattr(func, "__name__"):
        return func.__name__
    elif hasattr(func, "__class__"):
        return func.__class__.__name__
    return repr(func)


def _barrier_key(source: str | list[str], target: str) -> str:
    if isinstance(source, list):
        senders = "|".join(sorted(source))
        return f"barrier:{senders}->{target}"
    return f"barrier:{source}->{target}"
