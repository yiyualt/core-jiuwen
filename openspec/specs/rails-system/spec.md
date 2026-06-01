## ADDED Requirements

### Requirement: BaseRail
系统 SHALL 提供 `BaseRail` ABC，定义 `before(inputs, session)` 和 `after(result, session)` 钩子。

#### Scenario: Default pass-through
- **WHEN** 创建空 BaseRail 子类，调用 before/after
- **THEN** 返回原始输入/输出不变

### Requirement: RailPipeline
`RailPipeline` SHALL 按顺序执行 before → agent.run → after（逆序）。

#### Scenario: Pipeline execution order
- **WHEN** pipeline 有 [A, B] 两个 rail
- **THEN** 执行顺序为 A.before → B.before → agent.run → B.after → A.after

### Requirement: SecurityRail
`SecurityRail` SHALL 检测输入中的危险内容并阻止执行。

#### Scenario: Block dangerous query
- **WHEN** 输入包含 "DROP TABLE"
- **THEN** before() 返回拦截结果，agent 不被调用

#### Scenario: Pass safe query
- **WHEN** 输入为普通文本
- **THEN** before() 返回原始输入
