Graph Philosophy: The Pregel Execution Model
============================================

Why a Graph Engine?
-------------------

Workflows are DAGs (directed acyclic graphs). Each node is a component
that processes data. Edges define how data flows from one component to
the next. The graph engine is responsible for:

1. **Building** the DAG (adding nodes and edges)
2. **Compiling** it into an executable form
3. **Running** it with correct ordering and concurrency

The Pregel Model
----------------

jiuwen adapts Google's `Pregel <https://en.wikipedia.org/wiki/Pregel>`_
model for workflow execution. The key insight: nodes communicate through
**channels**, not direct function calls.

Execution proceeds in **super-steps**:

.. code-block:: text

    Super-step N:
      1. Check channels → which nodes are ready?
      2. Execute ready nodes concurrently (async)
      3. Route outputs → downstream channels
      4. Repeat until no ready nodes

This model naturally handles:
- **Concurrency**: independent nodes run in parallel
- **Fan-in**: a node waits for ALL upstreams (BarrierChannel)
- **Fan-out**: a node triggers multiple downstreams

Channel Types
-------------

.. list-table::
   :header-rows: 1

   * - Channel
     - Behavior
     - Use Case
   * - TriggerChannel
     - Ready when **any** message arrives (OR gate)
     - Simple A→B edge
   * - BarrierChannel
     - Ready when **all** expected senders arrive (AND gate)
     - N→1 fan-in, wait_for_all

.. code-block::

    TriggerChannel:            BarrierChannel:
      A ──→ [T] ──→ B           A ──╮
      (B ready when A fires)    B ──→ [B] ──→ C
                                (C ready when A AND B fire)

Executable: The Node Interface
------------------------------

Every node in the graph is an ``Executable``. It defines four I/O modes:

+------------------+------------------+-------------------------+
| Mode             | Input            | Output                  |
+==================+==================+=========================+
| ``on_invoke``    | batch (dict)     | batch (dict)            |
+------------------+------------------+-------------------------+
| ``on_stream``    | batch (dict)     | stream (async iterator) |
+------------------+------------------+-------------------------+
| ``on_collect``   | stream           | batch (dict)            |
+------------------+------------------+-------------------------+
| ``on_transform`` | stream           | stream (async iterator) |
+------------------+------------------+-------------------------+

v0.0.2 implements only ``on_invoke``. Other modes raise
``NotImplementedError`` — they'll be filled in by future versions.
