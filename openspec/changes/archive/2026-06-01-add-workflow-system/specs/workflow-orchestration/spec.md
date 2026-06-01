## ADDED Requirements

### Requirement: Workflow construction
`Workflow` 类 SHALL 封装 `WorkflowCard` 和 `PregelGraph`，提供组件注册和连接接口。

#### Scenario: Default construction with auto-generated card
- **WHEN** 创建 `Workflow()`
- **THEN** `wf.card` 不为 None，`wf.card.id` 自动生成

#### Scenario: Construction with custom card
- **WHEN** 创建 `Workflow(card=my_card)`
- **THEN** `wf.card is my_card`

### Requirement: Component registration
`Workflow` SHALL 支持 `set_start_comp`、`add_workflow_comp`、`set_end_comp` 注册组件。

#### Scenario: Register start component
- **WHEN** 调用 `wf.set_start_comp("entry", comp)`
- **THEN** 组件注册到 workflow，`wf.get_components()` 包含 "entry"

#### Scenario: Register same component as start and end
- **WHEN** 同一 ID 调用 `set_start_comp("main", comp)` 再调用 `set_end_comp("main", comp)`
- **THEN** 不抛异常，组件同时标记为 start 和 end

#### Scenario: Register intermediate component
- **WHEN** 调用 `wf.add_workflow_comp("middle", comp)`
- **THEN** 组件注册但不标记为 start 或 end

### Requirement: Connection management
`Workflow` SHALL 支持 `add_connection(src, tgt)` 和 `add_conditional_connection(src, router)`。

#### Scenario: Add connection
- **WHEN** 调用 `wf.add_connection("a", "b")`
- **THEN** 底层的 PregelGraph 记录了边 a→b

#### Scenario: Fluent API
- **WHEN** 链式调用 `wf.set_start_comp(...).add_workflow_comp(...).add_connection(...)`
- **THEN** 所有调用有效，返回 Self

### Requirement: Workflow execution
`Workflow.invoke(inputs)` SHALL 编译并执行底层 PregelGraph，返回 `WorkflowOutput`。

#### Scenario: Successful execution
- **WHEN** 调用 `await wf.invoke({"key": "val"})`
- **THEN** 返回 `WorkflowOutput` 且 `state == WorkflowExecutionState.COMPLETED`

#### Scenario: Error handling
- **WHEN** 组件执行中抛出异常
- **THEN** 返回 `WorkflowOutput` 且 `state == WorkflowExecutionState.ERROR`
