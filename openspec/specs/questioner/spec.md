## ADDED Requirements

### Requirement: QuestionerComponent asks when input missing
当指定字段不存在时，返回追问提示而非继续执行。

#### Scenario: Missing field returns question
- **WHEN** 调用 `invoke({})` 且期望字段不存在
- **THEN** 返回 `{"question": "...", "field": "..."}`

#### Scenario: Field present passes through
- **WHEN** 调用 `invoke({"name": "Alice"})` 且 field_name="name"
- **THEN** 返回 `{"output": "Alice"}`
