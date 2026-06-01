## 1. LLM Foundation Module

- [x] 1.1 Create `jiuwen/core/foundation/__init__.py`
- [x] 1.2 Create `jiuwen/core/foundation/llm.py` — ModelClientConfig, ModelRequestConfig, LLMClient ABC, FakeLLMClient
- [x] 1.3 Update `tests/conftest.py` — import FakeLLMClient from jiuwen.core.foundation.llm

## 2. Tests

- [x] 2.1 Create `tests/unit_tests/core/foundation/` with `__init__.py`
- [x] 2.2 Create `tests/unit_tests/core/foundation/test_llm.py` — test configs, LLMClient ABC, FakeLLMClient

## 3. Documentation

- [x] 3.1 Create `docs/jiuwen/notes/llm-foundation-philosophy.rst`
- [x] 3.2 Create `docs/jiuwen/examples/llm-example.rst`
- [x] 3.3 Create `docs/jiuwen/api/foundation.rst`
- [x] 3.4 Update toctrees

## 4. Verification

- [x] 4.1 Run all tests: `uv run pytest tests/ -v`
- [x] 4.2 Build docs: `rm -rf docs/_build && uv run sphinx-build -b html docs/ docs/_build/html` with zero warnings
