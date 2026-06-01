## 1. LLM Component

- [ ] 1.1 Create `jiuwen/core/workflow/components/llm/__init__.py`
- [ ] 1.2 Create `jiuwen/core/workflow/components/llm/llm_comp.py` — LLMCompConfig + LLMComponent
- [ ] 1.3 Update `jiuwen/core/workflow/components/__init__.py` to export LLMComponent and LLMCompConfig
- [ ] 1.4 Update `jiuwen/core/workflow/__init__.py` to export LLMComponent and LLMCompConfig

## 2. Tests

- [ ] 2.1 Create `tests/unit_tests/core/workflow/test_llm_component.py`

## 3. Documentation

- [ ] 3.1 Create `docs/jiuwen/notes/llm-component-philosophy.rst`
- [ ] 3.2 Create `docs/jiuwen/examples/llm-component-example.rst`
- [ ] 3.3 Update `docs/jiuwen/api/components.rst` with LLMComponent and LLMCompConfig
- [ ] 3.4 Update toctrees

## 4. Verification

- [ ] 4.1 Run all tests: `uv run pytest tests/ -v`
- [ ] 4.2 Build docs: `rm -rf docs/_build && uv run sphinx-build -b html docs/ docs/_build/html` with zero warnings
