## 1. Infrastructure Setup

- [x] 1.1 Add docs dependencies (sphinx, sphinx-book-theme) to pyproject.toml
- [x] 1.2 Create docs/conf.py with sphinx-book-theme configuration
- [x] 1.3 Create docs/index.rst with top-level toctree
- [x] 1.4 Verify `sphinx-build -b html docs/ docs/_build/html` builds without errors

## 2. Tutorials

- [x] 2.1 Create docs/jiuwen/tutorials/index.rst
- [x] 2.2 Create docs/jiuwen/tutorials/getting-started.rst with installation and first BaseCard example

## 3. Notes (Philosophy)

- [x] 3.1 Create docs/jiuwen/notes/index.rst
- [x] 3.2 Create docs/jiuwen/notes/basecard-philosophy.rst explaining Card/Config split

## 4. Examples

- [x] 4.1 Create docs/jiuwen/examples/index.rst
- [x] 4.2 Create docs/jiuwen/examples/basecard-example.rst with runnable code examples

## 5. API Reference

- [x] 5.1 Create docs/jiuwen/api/index.rst
- [x] 5.2 Create docs/jiuwen/api/common.rst documenting BaseCard fields and methods

## 6. Verification

- [x] 6.1 Full build: `rm -rf docs/_build && sphinx-build -b html docs/ docs/_build/html` passes with zero warnings
- [x] 6.2 All existing tests still pass: `uv run pytest tests/ -v`
