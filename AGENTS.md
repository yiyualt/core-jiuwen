# AGENTS.md

Shared instructions for AI coding assistants working in `core-jiuwen`.

## What This Repo Is

- `jiuwen/core/`: public SDK/runtime for agents, workflows, and LLM integration.
- `tests/`: fast deterministic unit tests with FakeLLM — no real API calls.
- `docs/`: user-facing documentation.

## Architecture Principles

- **Card/Config split**: Cards = static metadata (serializable, pydantic BaseModel).
  Configs = runtime objects holding resources and state.
- **Component-based workflows**: DAG of components with typed I/O.
- **Async-first**: all execution is async.
- **FakeLLM for tests**: no real API dependencies.

## Commands

- Setup: `uv sync`
- Run tests: `make test`
- Run targeted test: `make test TESTFLAGS="tests/unit_tests/path/to/test.py"`
- Lint: `make check`
- Auto-fix: `make fix`

## Code Style

- Python 3.11+
- Ruff line length: 120
- All English: docs, comments, commit messages
- Tests mirror source: `jiuwen/core/foo.py` → `tests/unit_tests/core/test_foo.py`
