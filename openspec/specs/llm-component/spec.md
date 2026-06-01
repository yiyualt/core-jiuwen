## ADDED Requirements

### Requirement: LLMCompConfig configuration
`LLMCompConfig` SHALL 封装 model_client_config、model_config、template_content 和 output_config。

#### Scenario: Full configuration
- **WHEN** 创建包含全部四个字段的 LLMCompConfig
- **THEN** 所有字段可正确访问

### Requirement: LLMComponent template rendering
`LLMComponent` SHALL 在 invoke 时将模板中的 `{{变量}}` 替换为 inputs 中的实际值。

#### Scenario: Render template with inputs
- **WHEN** 模板为 `[{"role": "user", "content": "{{query}}"}]`，调用 invoke({"query": "hello"})
- **THEN** 实际发送给 LLMClient 的消息为 `[{"role": "user", "content": "hello"}]`

### Requirement: LLMComponent invokes LLMClient
`LLMComponent.invoke(inputs)` SHALL 渲染模板后调用 `client.chat(messages, config)`，返回结果。

#### Scenario: Invoke with FakeLLMClient
- **WHEN** 注入 FakeLLMClient(["Hello!"]) 并调用 invoke
- **THEN** 返回包含 LLM 响应的 dict

### Requirement: End-to-end pipeline
Start → LLMComponent → End pipeline SHALL 可正确执行。

#### Scenario: Complete pipeline
- **WHEN** workflow 包含 Start + LLMComponent(with FakeLLMClient) + End，调用 invoke({"query": "hi"})
- **THEN** 返回 COMPLETED 状态，End 的模板渲染包含 LLM 响应
