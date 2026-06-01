## ADDED Requirements

### Requirement: ToolCard extends BaseCard
`ToolCard` SHALL 继承 `BaseCard`，增加 `parameters` 和 `func` 字段。

#### Scenario: Default construction
- **WHEN** 创建 `ToolCard()`
- **THEN** parameters 为 None，func 为 None

#### Scenario: Full construction
- **WHEN** 创建 `ToolCard(name="search", parameters={...}, func=my_func)`
- **THEN** 所有字段正确赋值

#### Scenario: tool_info returns structured metadata
- **WHEN** 调用 `card.tool_info()`
- **THEN** 返回 `{"name": ..., "description": ..., "parameters": {...}}`

### Requirement: Pydantic serialization excludes func
`ToolCard` 的序列化 SHALL 排除 `func` 字段。

#### Scenario: model_dump excludes func
- **WHEN** 调用 `card.model_dump()`
- **THEN** 结果不包含 "func" 键
