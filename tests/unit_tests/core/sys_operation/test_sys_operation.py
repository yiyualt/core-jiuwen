# coding: utf-8
"""Tests for CodeOperator, ShellOperator, and FileOperator."""

import tempfile
import pytest
from jiuwen.core.sys_operation import OperationResult, CodeOperator, ShellOperator, FileOperator


class TestCodeOperator:
    @pytest.mark.asyncio
    async def test_simple_code(self):
        op = CodeOperator(timeout=5)
        result = await op.execute("print(1+1)")
        assert result.success
        assert "2" in result.output

    @pytest.mark.asyncio
    async def test_syntax_error(self):
        op = CodeOperator()
        result = await op.execute("invalid python code !!!")
        assert not result.success

    @pytest.mark.asyncio
    async def test_timeout(self):
        op = CodeOperator(timeout=0.1)
        result = await op.execute("while True: pass")
        assert not result.success
        assert "timed out" in (result.error or "")


class TestShellOperator:
    @pytest.mark.asyncio
    async def test_allowed_command(self):
        op = ShellOperator(allowed_commands=["echo"])
        result = await op.execute("echo hello")
        assert result.success
        assert "hello" in result.output

    @pytest.mark.asyncio
    async def test_blocked_command(self):
        op = ShellOperator(allowed_commands=["ls"])
        result = await op.execute("rm file")
        assert not result.success
        assert "not allowed" in (result.error or "")

    @pytest.mark.asyncio
    async def test_all_allowed(self):
        op = ShellOperator()  # no whitelist
        result = await op.execute("echo test")
        assert result.success


class TestFileOperator:
    def test_write_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            op = FileOperator(tmp)
            w = op.write("test.txt", "hello")
            assert w.success
            r = op.read("test.txt")
            assert r.success
            assert r.output == "hello"

    def test_list_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            op = FileOperator(tmp)
            op.write("a.py", "1")
            op.write("b.py", "2")
            result = op.list("*.py")
            assert result.success
            assert len(result.output.splitlines()) == 2

    def test_nonexistent(self):
        op = FileOperator("/tmp")
        r = op.read("nonexistent_xyz_file.txt")
        assert not r.success

    def test_path_escape(self):
        op = FileOperator("/tmp")
        r = op.write("../etc/passwd", "evil")
        assert not r.success
        assert "escapes" in (r.error or "")
