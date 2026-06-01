## 1. Executable Abstraction

- [x] 1.1 Create `jiuwen/core/graph/executable.py` — Executable ABC with 4 I/O modes + GeneralExecutor type alias
- [x] 1.2 Create `tests/unit_tests/core/graph/test_executable.py` — test NotImplementedError defaults and custom implementations

## 2. Channel System

- [x] 2.1 Create `jiuwen/core/graph/channels.py` — Channel ABC, TriggerChannel, BarrierChannel
- [x] 2.2 Create `tests/unit_tests/core/graph/test_channels.py` — test OR/AND semantics, snapshot/restore

## 3. Graph Construction

- [x] 3.1 Create `jiuwen/core/graph/base.py` — Graph ABC, Router type, ExecutableGraph base
- [x] 3.2 Create `jiuwen/core/graph/graph.py` — PregelGraph (builder) + CompiledGraph (executor)
- [x] 3.3 Create `tests/unit_tests/core/graph/test_graph.py` — test construction, compilation, execution

## 4. Package Integration

- [x] 4.1 Create `jiuwen/core/graph/__init__.py` — export all public symbols

## 5. Documentation

- [x] 5.1 Create `docs/jiuwen/notes/graph-philosophy.rst` — Pregel model explanation
- [x] 5.2 Create `docs/jiuwen/examples/graph-example.rst` — runnable graph examples
- [x] 5.3 Create `docs/jiuwen/api/graph.rst` — API reference
- [x] 5.4 Update `docs/jiuwen/notes/index.rst` and `docs/jiuwen/examples/index.rst` and `docs/jiuwen/api/index.rst` toctrees

## 6. Verification

- [x] 6.1 Run all tests: `uv run pytest tests/ -v` (expected: 14 + new tests all pass)
- [x] 6.2 Build docs: `rm -rf docs/_build && uv run sphinx-build -b html docs/ docs/_build/html` with zero warnings
