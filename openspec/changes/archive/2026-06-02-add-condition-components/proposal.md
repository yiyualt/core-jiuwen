## Why

Workflow 目前只能线性执行。Condition 组件让工作流支持分支（if/else）和循环，从 DAG 升级为真正的控制流引擎。

## What Changes

- 新增 `jiuwen/core/workflow/components/condition/` — Condition ABC + ExpressionCondition
- 新增 `jiuwen/core/workflow/components/flow/branch_comp.py` — BranchComponent + BranchRouter
- 更新 Workflow 支持 add_conditional_connection

## Capabilities

### New Capabilities
- `condition-system`: 条件评估抽象（ExpressionCondition）
- `branch-component`: 分支组件，根据条件路由到不同下游节点

## Impact

- 新增 condition/ 和 flow/branch_comp.py
- 测试 + 文档
