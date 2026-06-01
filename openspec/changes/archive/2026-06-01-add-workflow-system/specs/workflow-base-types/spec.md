## ADDED Requirements

### Requirement: WorkflowCard extends BaseCard
`WorkflowCard` SHALL 继承 `BaseCard`，新增 `version` 和 `input_params` 字段。

#### Scenario: Default construction
- **WHEN** 创建 `WorkflowCard()`
- **THEN** `version` 为空字符串，`input_params` 为 None，同时继承 `id`、`name`、`description`

#### Scenario: Full construction
- **WHEN** 创建 `WorkflowCard(id="wf-1", name="文本生成", version="2.0", description="生成文本", input_params={...})`
- **THEN** 所有字段正确赋值

#### Scenario: tool_info returns structured metadata
- **WHEN** 调用 `card.tool_info()`
- **THEN** 返回 `{"name": ..., "description": ..., "parameters": ...}`

### Requirement: WorkflowExecutionState enum
系统 SHALL 定义 `WorkflowExecutionState` 枚举，包含 COMPLETED、INPUT_REQUIRED、ERROR 三个值。

#### Scenario: Enum values
- **WHEN** 访问枚举值
- **THEN** `COMPLETED.value == "COMPLETED"`, `ERROR.value == "ERROR"`, `INPUT_REQUIRED.value == "INPUT_REQUIRED"`

### Requirement: WorkflowOutput container
`WorkflowOutput` SHALL 是 Pydantic BaseModel，包含 `result` 和 `state` 字段。

#### Scenario: Success output
- **WHEN** 创建 `WorkflowOutput(result={"key": "val"}, state=WorkflowExecutionState.COMPLETED)`
- **THEN** `model_dump()` 正确序列化

### Requirement: generate_workflow_key utility
`generate_workflow_key(workflow_id, workflow_version)` SHALL 返回 `"{id}_{version}"` 格式的字符串。

#### Scenario: Key generation
- **WHEN** 调用 `generate_workflow_key("my_flow", "1.0")`
- **THEN** 返回 `"my_flow_1.0"`
