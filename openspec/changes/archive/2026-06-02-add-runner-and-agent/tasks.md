## 1. Runner

- [x] 1.1 Create `jiuwen/core/runner/` with `__init__.py`, `runner.py`
- [x] 1.2 Create `tests/unit_tests/core/runner/` with `test_runner.py`

## 2. Agent System

- [x] 2.1 Create `jiuwen/core/single_agent/` with `__init__.py`, `legacy.py`
- [x] 2.2 Create `tests/unit_tests/core/single_agent/` with `test_agent.py`

## 3. Documentation

- [x] 3.1 Create `docs/jiuwen/notes/runner-philosophy.rst`
- [x] 3.2 Create `docs/jiuwen/notes/agent-philosophy.rst`
- [x] 3.3 Create `docs/jiuwen/examples/runner-example.rst`
- [x] 3.4 Create `docs/jiuwen/api/` entries for runner and agent
- [x] 3.5 Update toctrees

## 4. Verification

- [x] 4.1 Run all tests: `uv run pytest tests/ -v`
- [x] 4.2 Build docs: `rm -rf docs/_build && uv run sphinx-build -b html docs/ docs/_build/html` with zero warnings
