## ADDED Requirements

### Requirement: Start component
`Start` 组件 SHALL 透传输入数据，不做任何转换。

#### Scenario: Pass through inputs
- **WHEN** 调用 `await start.invoke({"query": "hello", "count": 5})`
- **THEN** 返回 `{"query": "hello", "count": 5}`

#### Scenario: Empty inputs
- **WHEN** 调用 `await start.invoke({})`
- **THEN** 返回 `{}`

### Requirement: End component no template
不带模板的 `End` 组件 SHALL 将输入包装为 `{"output": inputs}`，过滤 None 值。

#### Scenario: Wrap outputs
- **WHEN** 调用 `await end.invoke({"text": "hello"})`
- **THEN** 返回 `{"output": {"text": "hello"}}`

#### Scenario: Filter None values
- **WHEN** 调用 `await end.invoke({"a": "val", "b": None})`
- **THEN** 返回 `{"output": {"a": "val"}}`

### Requirement: End component with template
带 `responseTemplate` 的 `End` 组件 SHALL 使用 Python `string.Template` 渲染输出。

#### Scenario: Render template
- **WHEN** 创建 `End({"responseTemplate": "结果: {{output}}"})` 并调用 `invoke({"output": "hello"})`
- **THEN** 返回 `{"response": "结果: hello"}`

#### Scenario: Missing variable handled gracefully
- **WHEN** 模板中变量在 inputs 中不存在
- **THEN** 使用 `$varname` 作为占位符（safe_substitute 行为）

### Requirement: End component stream
`End.stream(inputs)` SHALL 逐个产出 key-value 对，或渲染模板后产出单个结果。

#### Scenario: Stream with template
- **WHEN** 调用 `end.stream({"data": "test"})`
- **THEN** yield 单个 `{"response": "..."}` 结果

#### Scenario: Stream without template
- **WHEN** 调用 `end.stream({"a": "1", "b": "2"})`
- **THEN** yield 两个独立的 output 块
