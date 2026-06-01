# coding: utf-8
"""Graph execution engine for jiuwen workflows.

Provides the Pregel-based graph execution model:
- Executable: base class for invokable components
- PregelGraph: DAG construction and compilation
- Channels: trigger and barrier message passing
"""

from jiuwen.core.graph.executable import Executable, Input, Output, GeneralExecutor
from jiuwen.core.graph.base import Graph, Router, ExecutableGraph
from jiuwen.core.graph.graph import PregelGraph, CompiledGraph
from jiuwen.core.graph.channels import TriggerChannel, BarrierChannel, Channel

__all__ = [
    "Executable",
    "Input",
    "Output",
    "GeneralExecutor",
    "Graph",
    "Router",
    "ExecutableGraph",
    "PregelGraph",
    "CompiledGraph",
    "TriggerChannel",
    "BarrierChannel",
    "Channel",
]
