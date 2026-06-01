## 1. Dependencies

- [x] 1.1 Add `openai` and `python-dotenv` to pyproject.toml dependencies
- [x] 1.2 Create `.env.example` template

## 2. OpenAIClient

- [x] 2.1 Add `OpenAIClient` to `jiuwen/core/foundation/llm.py`
- [x] 2.2 Remove `FakeLLMClient` from `jiuwen/core/foundation/llm.py`
- [x] 2.3 Move `FakeLLMClient` to `tests/conftest.py`
- [x] 2.4 Update `jiuwen/core/foundation/__init__.py`

## 3. LLMComponent

- [x] 3.1 Change default client to `OpenAIClient.from_env()`
- [x] 3.2 Update `tests/unit_tests/core/workflow/test_llm_component.py`

## 4. Documentation

- [x] 4.1 Rewrite `docs/jiuwen/notes/llm-foundation-philosophy.rst`
- [x] 4.2 Rewrite `docs/jiuwen/notes/llm-component-philosophy.rst`
- [x] 4.3 Rewrite `docs/jiuwen/examples/llm-example.rst`
- [x] 4.4 Rewrite `docs/jiuwen/examples/llm-component-example.rst`
- [x] 4.5 Update `docs/jiuwen/api/foundation.rst`
- [x] 4.6 Update `docs/jiuwen/api/components.rst`

## 5. Verification

- [x] 5.1 Run all tests: `uv run pytest tests/ -v`
- [x] 5.2 Build docs: `rm -rf docs/_build && uv run sphinx-build -b html docs/ docs/_build/html` with zero warnings
