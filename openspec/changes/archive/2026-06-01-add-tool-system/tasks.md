## 1. Tool Foundation

- [ ] 1.1 Create `jiuwen/core/foundation/tool.py` — ToolCard + ToolComponent
- [ ] 1.2 Update `jiuwen/core/foundation/__init__.py` to export ToolCard and ToolComponent

## 2. Tests

- [ ] 2.1 Create `tests/unit_tests/core/foundation/test_tool.py`

## 3. Documentation

- [ ] 3.1 Create `docs/jiuwen/notes/tool-system-philosophy.rst`
- [ ] 3.2 Create `docs/jiuwen/examples/tool-example.rst`
- [ ] 3.3 Create `docs/jiuwen/api/tool.rst`
- [ ] 3.4 Update toctrees

## 4. Verification

- [ ] 4.1 Run all tests: `uv run pytest tests/ -v`
- [ ] 4.2 Build docs: `rm -rf docs/_build && uv run sphinx-build -b html docs/ docs/_build/html` with zero warnings
