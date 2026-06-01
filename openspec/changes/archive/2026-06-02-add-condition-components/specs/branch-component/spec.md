## ADDED Requirements

### Requirement: BranchComponent
`BranchComponent` SHALL 包装 Condition 并在 invoke 时返回 `{"branch_result": bool}`。

#### Scenario: True branch
- **WHEN** `BranchComponent(ExpressionCondition("{{ready}} == True")).invoke({"ready": True})`
- **THEN** 返回 `{"branch_result": True}`

### Requirement: Conditional routing in Workflow
Workflow 的 `add_conditional_connection` SHALL 支持根据 BranchComponent 输出路由。

#### Scenario: If-else routing
- **WHEN** workflow 包含 BranchComponent + 两个下游，条件为 True
- **THEN** 数据流入 True 分支
