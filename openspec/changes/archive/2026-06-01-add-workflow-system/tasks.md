## 1. Workflow Base Types

- [x] 1.1 Create `jiuwen/core/workflow/base.py` — WorkflowCard, WorkflowExecutionState, WorkflowOutput, generate_workflow_key
- [x] 1.2 Create `tests/unit_tests/core/workflow/test_base.py` — test all base types

## 2. Component System

- [x] 2.1 Create `jiuwen/core/workflow/components/base.py` — ComponentAbility, ComponentConfig, WorkflowComponentMetadata
- [x] 2.2 Create `jiuwen/core/workflow/components/component.py` — ComponentExecutable, ComponentComposable, WorkflowComponent
- [x] 2.3 Create `jiuwen/core/workflow/components/flow/start_comp.py` — Start component
- [x] 2.4 Create `jiuwen/core/workflow/components/flow/end_comp.py` — End component + EndConfig
- [x] 2.5 Create `tests/unit_tests/core/workflow/test_components.py` — test components

## 3. Workflow Orchestration

- [x] 3.1 Create `jiuwen/core/workflow/workflow.py` — Workflow class
- [x] 3.2 Create `jiuwen/core/workflow/__init__.py` — export all
- [x] 3.3 Create `tests/unit_tests/core/workflow/test_workflow.py` — test workflow construction and execution

## 4. Documentation

- [x] 4.1 Create `docs/jiuwen/notes/workflow-philosophy.rst`
- [x] 4.2 Create `docs/jiuwen/notes/component-philosophy.rst`
- [x] 4.3 Create `docs/jiuwen/examples/workflow-example.rst`
- [x] 4.4 Create `docs/jiuwen/examples/component-example.rst`
- [x] 4.5 Create `docs/jiuwen/api/workflow.rst` and `docs/jiuwen/api/components.rst`
- [x] 4.6 Update toctrees in notes/examples/api index.rst

## 5. Verification

- [x] 5.1 Run all tests: `uv run pytest tests/ -v`
- [x] 5.2 Build docs: `rm -rf docs/_build && uv run sphinx-build -b html docs/ docs/_build/html` with zero warnings
