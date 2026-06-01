# coding: utf-8
"""Tests for the Executable base class."""

import pytest
from jiuwen.core.graph.executable import Executable


class TestExecutableDefaults:
    """Tests for default (unimplemented) behavior."""

    def test_on_invoke_raises_not_implemented(self):
        class MyExe(Executable):
            pass

        exe = MyExe()
        with pytest.raises(NotImplementedError, match="MyExe"):
            import asyncio
            asyncio.run(exe.on_invoke({"k": "v"}))

    def test_on_stream_raises_not_implemented(self):
        class MyExe(Executable):
            pass

        exe = MyExe()
        with pytest.raises(NotImplementedError, match="MyExe"):
            import asyncio
            coro = exe.on_stream({"k": "v"})
            asyncio.run(coro)

    def test_on_collect_raises_not_implemented(self):
        class MyExe(Executable):
            pass

        exe = MyExe()
        with pytest.raises(NotImplementedError, match="MyExe"):
            import asyncio
            async def gen():
                yield {"d": 1}
            asyncio.run(exe.on_collect(gen()))

    def test_on_transform_raises_not_implemented(self):
        class MyExe(Executable):
            pass

        exe = MyExe()
        with pytest.raises(NotImplementedError, match="MyExe"):
            import asyncio
            async def gen():
                yield {"d": 1}
            coro = exe.on_transform(gen())
            asyncio.run(coro)

    def test_skip_trace_default(self):
        assert Executable().skip_trace() is False

    def test_post_commit_default(self):
        assert Executable().post_commit() is True

    def test_graph_invoker_default(self):
        assert Executable().graph_invoker() is False

    def test_component_type_default(self):
        assert Executable().component_type() == ""


class TestExecutableSubclass:
    """Tests for properly implemented subclasses."""

    @pytest.mark.asyncio
    async def test_custom_invoke(self):
        class Adder(Executable[dict, dict]):
            async def on_invoke(self, inputs: dict, **kwargs) -> dict:
                return {"sum": inputs["a"] + inputs["b"]}

        result = await Adder().on_invoke({"a": 3, "b": 4})
        assert result == {"sum": 7}

    @pytest.mark.asyncio
    async def test_custom_stream(self):
        class Counter(Executable[dict, int]):
            async def on_stream(self, inputs: dict, **kwargs):
                for i in range(inputs.get("count", 0)):
                    yield i

        results = []
        async for val in Counter().on_stream({"count": 3}):
            results.append(val)
        assert results == [0, 1, 2]

    @pytest.mark.asyncio
    async def test_custom_collect(self):
        class Summer(Executable[int, dict]):
            async def on_collect(self, inputs, **kwargs) -> dict:
                total = 0
                async for val in inputs:
                    total += val
                return {"total": total}

        async def gen():
            for i in [1, 2, 3]:
                yield i

        result = await Summer().on_collect(gen())
        assert result == {"total": 6}
