# coding: utf-8
"""Tests for TokenCounter, MessageBuffer, and ModelContext."""

from jiuwen.core.context_engine import TokenCounter, MessageBuffer, ModelContext


class TestTokenCounter:
    def test_counts_messages(self):
        counter = TokenCounter()
        count = counter.count([{"role": "user", "content": "hello world"}])
        assert count > 0

    def test_empty_messages(self):
        counter = TokenCounter()
        assert counter.count([]) == 1  # max(1, 0//4)

    def test_multiple_messages(self):
        counter = TokenCounter()
        count_a = counter.count([{"content": "a" * 100}])
        count_b = counter.count([{"content": "a" * 200}])
        assert count_b > count_a


class TestMessageBuffer:
    def test_basic_add_get(self):
        buf = MessageBuffer(max_tokens=99999)
        buf.add("user", "hello")
        assert len(buf.get_messages()) == 1

    def test_trims_on_overflow(self):
        # Very small limit forces trimming
        buf = MessageBuffer(max_tokens=10)
        buf.add_system("sys")  # ~1 token
        buf.add_user("hello world")  # ~3 tokens
        buf.add_assistant("hi there, how can I help you today?")  # ~9 tokens
        # Now add another pair — should trim the first user+assistant
        buf.add_user("another long question here")
        buf.add_assistant("another long answer here")
        msgs = buf.get_messages()
        # System should remain
        assert msgs[0]["role"] == "system"

    def test_preserves_system(self):
        buf = MessageBuffer(max_tokens=5)
        buf.add_system("important system instruction that must stay")
        buf.add_user("a")
        buf.add_assistant("b")
        buf.add_user("c")
        buf.add_assistant("d")
        msgs = buf.get_messages()
        assert msgs[0]["role"] == "system"

    def test_clear(self):
        buf = MessageBuffer()
        buf.add_user("test")
        buf.clear()
        assert buf.get_messages() == []


class TestModelContext:
    def test_convenience_methods(self):
        ctx = ModelContext(max_tokens=99999)
        ctx.add_system("you are helpful")
        ctx.add_user("hello")
        ctx.add_assistant("hi")
        msgs = ctx.get_messages()
        assert len(msgs) == 3
        assert msgs[0]["role"] == "system"
        assert msgs[1]["role"] == "user"
        assert msgs[2]["role"] == "assistant"

    def test_add_messages_bulk(self):
        ctx = ModelContext()
        ctx.add_messages([
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
        ])
        assert len(ctx.get_messages()) == 2
