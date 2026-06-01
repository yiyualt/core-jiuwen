# coding: utf-8
"""Tests for TriggerChannel and BarrierChannel."""

import pytest
from jiuwen.core.graph.channels import TriggerChannel, BarrierChannel
from jiuwen.core.graph.graph import TriggerMessage, BarrierMessage


class TestTriggerChannel:
    def test_not_ready_initially(self):
        ch = TriggerChannel("n")
        assert ch.is_ready() is False

    def test_ready_after_accept(self):
        ch = TriggerChannel("n")
        ch.accept(TriggerMessage(sender="s", target="n"))
        assert ch.is_ready() is True

    def test_not_ready_after_consume(self):
        ch = TriggerChannel("n")
        ch.accept(TriggerMessage(sender="s", target="n"))
        ch.consume()
        assert ch.is_ready() is False

    def test_accept_returns_true(self):
        assert TriggerChannel("n").accept(TriggerMessage(sender="x", target="n")) is True

    def test_key(self):
        assert TriggerChannel("my").key == "channel:my"
        assert TriggerChannel("my").node_name == "my"

    def test_snapshot_restore(self):
        ch = TriggerChannel("n")
        ch.accept(TriggerMessage(sender="a", target="n"))
        ch.accept(TriggerMessage(sender="b", target="n"))
        snap = ch.snapshot()
        ch2 = TriggerChannel("n")
        ch2.restore(snap)
        assert ch2.is_ready() is True


class TestBarrierChannel:
    def test_not_ready_initially(self):
        ch = BarrierChannel("n", {"a", "b"})
        assert ch.is_ready() is False

    def test_not_ready_partial(self):
        ch = BarrierChannel("n", {"a", "b"})
        ch.accept(BarrierMessage(sender="a", target="n"))
        assert ch.is_ready() is False

    def test_ready_all_arrived(self):
        ch = BarrierChannel("n", {"a", "b"})
        ch.accept(BarrierMessage(sender="a", target="n"))
        ch.accept(BarrierMessage(sender="b", target="n"))
        assert ch.is_ready() is True

    def test_duplicate_ignored(self):
        ch = BarrierChannel("n", {"a", "b"})
        assert ch.accept(BarrierMessage(sender="a", target="n")) is True
        assert ch.accept(BarrierMessage(sender="a", target="n")) is False

    def test_unknown_sender_ignored(self):
        ch = BarrierChannel("n", {"a"})
        assert ch.accept(BarrierMessage(sender="x", target="n")) is False
        assert ch.is_ready() is False

    def test_not_ready_after_consume(self):
        ch = BarrierChannel("n", {"a", "b"})
        ch.accept(BarrierMessage(sender="a", target="n"))
        ch.accept(BarrierMessage(sender="b", target="n"))
        ch.consume()
        assert ch.is_ready() is False

    def test_key_deterministic(self):
        a = BarrierChannel("n", {"b", "a"})
        b = BarrierChannel("n", {"a", "b"})
        assert a.key == b.key

    def test_message_without_sender(self):
        ch = BarrierChannel("n", {"a"})
        class Plain:
            pass
        assert ch.accept(Plain()) is False

    def test_snapshot_restore(self):
        ch = BarrierChannel("n", {"a", "b", "c"})
        ch.accept(BarrierMessage(sender="a", target="n"))
        ch.accept(BarrierMessage(sender="b", target="n"))
        snap = ch.snapshot()
        ch2 = BarrierChannel("n", {"a", "b", "c"})
        ch2.restore(snap)
        assert ch2.is_ready() is False  # still waiting for c
