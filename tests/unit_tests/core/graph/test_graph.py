# coding: utf-8
"""Tests for PregelGraph construction, compilation, and execution."""

import pytest
from jiuwen.core.graph.executable import Executable
from jiuwen.core.graph.graph import PregelGraph, CompiledGraph


class EchoNode(Executable[dict, dict]):
    def __init__(self, name: str):
        self.name = name

    async def on_invoke(self, inputs: dict, **kwargs) -> dict:
        return {self.name: f"echo:{inputs.get('value', '')}"}


class TransformNode(Executable[dict, dict]):
    def __init__(self, name: str, fn):
        self.name = name
        self.fn = fn

    async def on_invoke(self, inputs: dict, **kwargs) -> dict:
        return {self.name: self.fn(inputs)}


class TestConstruction:
    def test_empty(self):
        g = PregelGraph()
        assert len(g.get_nodes()) == 0

    def test_add_node(self):
        g = PregelGraph()
        g.add_node("n", EchoNode("n"))
        assert "n" in g.get_nodes()

    def test_duplicate_raises(self):
        g = PregelGraph()
        g.add_node("n", EchoNode("a"))
        with pytest.raises(ValueError, match="already exists"):
            g.add_node("n", EchoNode("b"))

    def test_none_raises(self):
        with pytest.raises(ValueError, match="is None"):
            PregelGraph().add_node("n", None)

    def test_empty_id_raises(self):
        with pytest.raises(ValueError):
            PregelGraph().add_node("", EchoNode("x"))

    def test_add_edge(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a"))
        g.add_node("b", EchoNode("b"))
        g.add_edge("a", "b")
        assert len(g.edges) == 1

    def test_add_edge_list_source(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a"))
        g.add_node("b", EchoNode("b"))
        g.add_node("c", EchoNode("c"))
        g.add_edge(["a", "b"], "c")
        assert len(g.edges) == 1

    def test_empty_source_raises(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a"))
        with pytest.raises(ValueError):
            g.add_edge("", "a")

    def test_empty_target_raises(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a"))
        with pytest.raises(ValueError):
            g.add_edge("a", "")

    def test_start_node(self):
        g = PregelGraph()
        g.add_node("entry", EchoNode("entry"))
        g.start_node("entry")
        assert "entry" in g._start_nodes

    def test_end_node(self):
        g = PregelGraph()
        g.add_node("exit", EchoNode("exit"))
        g.end_node("exit")
        assert "exit" in g._end_nodes

    def test_conditional_edges(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a"))
        g.add_conditional_edges("a", lambda s: "b")
        assert "a" in g.branches

    def test_empty_conditional_source_raises(self):
        with pytest.raises(ValueError):
            PregelGraph().add_conditional_edges("", lambda x: "b")

    def test_none_router_raises(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a"))
        with pytest.raises(ValueError):
            g.add_conditional_edges("a", None)

    def test_wait_for_all(self):
        g = PregelGraph()
        g.add_node("c", EchoNode("c"), wait_for_all=True)
        assert "c" in g.waits

    def test_fluent_api(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a")).add_node("b", EchoNode("b")).add_edge("a", "b").start_node("a").end_node("b")
        assert len(g.get_nodes()) == 2


class TestCompilation:
    def test_empty_compiles(self):
        compiled = PregelGraph().compile()
        assert isinstance(compiled, CompiledGraph)

    def test_simple_compiles(self):
        g = PregelGraph()
        g.add_node("a", EchoNode("a"))
        g.add_node("b", EchoNode("b"))
        g.add_edge("a", "b")
        g.start_node("a")
        g.end_node("b")
        assert isinstance(g.compile(), CompiledGraph)


class TestExecution:
    @pytest.mark.asyncio
    async def test_single_node(self):
        class Doubler(Executable[dict, dict]):
            async def on_invoke(self, inputs: dict, **kwargs) -> dict:
                return {"result": inputs.get("value", 0) * 2}

        g = PregelGraph()
        g.add_node("d", Doubler())
        g.start_node("d")
        g.end_node("d")
        result = await g.compile()._invoke({"value": 5})
        assert result["d"]["result"] == 10

    @pytest.mark.asyncio
    async def test_two_node_linear(self):
        class NodeA(Executable[dict, dict]):
            async def on_invoke(self, inputs: dict, **kwargs) -> dict:
                return {"val": inputs.get("value", 0) + 10}

        class NodeB(Executable[dict, dict]):
            async def on_invoke(self, inputs: dict, **kwargs) -> dict:
                return {"val": inputs.get("value", 0) * 2}

        g = PregelGraph()
        g.add_node("step1", NodeA())
        g.add_node("step2", NodeB())
        g.add_edge("step1", "step2")
        g.start_node("step1")
        g.end_node("step2")
        result = await g.compile()._invoke({"value": 5})
        assert "step2" in result

    @pytest.mark.asyncio
    async def test_multi_start(self):
        calls = []

        class Collector(Executable[dict, dict]):
            async def on_invoke(self, inputs: dict, **kwargs) -> dict:
                calls.append(inputs.get("name", ""))
                return {"name": inputs.get("name", "")}

        g = PregelGraph()
        g.add_node("w1", Collector())
        g.add_node("w2", Collector())
        g.start_node("w1")
        g.start_node("w2")
        await g.compile()._invoke({"name": "task"})
        assert len(calls) == 2

    @pytest.mark.asyncio
    async def test_not_implemented_propagates(self):
        class Broken(Executable):
            pass

        g = PregelGraph()
        g.add_node("b", Broken())
        g.start_node("b")
        with pytest.raises(NotImplementedError):
            await g.compile()._invoke({})
