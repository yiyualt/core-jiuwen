## ADDED Requirements

### Requirement: BaseSection defines build interface
`BaseSection` SHALL 定义 `build(context) → str` 抽象方法。

#### Scenario: Custom section
- **WHEN** 子类实现 `build(context)` 返回自定义字符串
- **THEN** `PromptBuilder.build()` 包含该 section 的输出

### Requirement: PromptBuilder composes sections
`PromptBuilder.build(context)` SHALL 将多个 section 的输出以双换行连接。

#### Scenario: Multiple sections combined
- **WHEN** builder 包含 [IdentitySection, ToolsSection]
- **THEN** build() 返回两段文字，中间以 `\n\n` 分隔

### Requirement: DeepAgent uses PromptBuilder
`DeepAgent` SHALL 接受可选的 `prompt_builder` 参数。

#### Scenario: Custom prompt builder
- **WHEN** 创建 DeepAgent(client, config, prompt_builder=custom_builder)
- **THEN** agent 使用 custom_builder.build() 作为 system prompt
