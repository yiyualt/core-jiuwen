# coding: utf-8
"""Tests for InputGuard, OutputGuard, and PathSecurity."""

import tempfile
from pathlib import Path

from jiuwen.core.security import InputGuard, OutputGuard, PathSecurity


class TestInputGuard:
    def test_blocks_dangerous(self):
        ok, reason = InputGuard.check("please rm -rf /tmp/cache")
        assert ok is False
        assert "rm -rf" in reason

    def test_blocks_drop_table(self):
        ok, _ = InputGuard.check("DROP TABLE users")
        assert ok is False

    def test_blocks_eval(self):
        ok, _ = InputGuard.check("eval('1+1')")
        assert ok is False

    def test_passes_safe(self):
        ok, reason = InputGuard.check("What is Python?")
        assert ok is True
        assert reason is None

    def test_case_insensitive(self):
        ok, _ = InputGuard.check("Please RM -RF tmp")
        assert ok is False


class TestOutputGuard:
    def test_passes_normal_output(self):
        ok, found = OutputGuard.check("Here is your Python code.")
        assert ok is True
        assert found == []

    def test_detects_api_key(self):
        ok, found = OutputGuard.check("My key is sk-abcdefghijklmnopqrstuvwxyz123456")
        assert ok is False
        assert len(found) > 0

    def test_detects_key_value_secret(self):
        ok, found = OutputGuard.check("password: hunter2")
        assert ok is False


class TestPathSecurity:
    def test_safe_path(self):
        assert PathSecurity.is_safe("/project", "src/main.py") is True

    def test_escape_blocked(self):
        assert PathSecurity.is_safe("/project", "../etc/passwd") is False

    def test_absolute_escape_blocked(self):
        assert PathSecurity.is_safe("/project", "/etc/hosts") is False

    def test_sanitize_returns_path(self):
        result = PathSecurity.sanitize("/tmp", "test.txt")
        assert result is not None

    def test_sanitize_returns_none_for_escape(self):
        result = PathSecurity.sanitize("/tmp", "../../root")
        assert result is None

    def test_real_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp, "subdir")
            p.mkdir()
            assert PathSecurity.is_safe(tmp, "subdir") is True
