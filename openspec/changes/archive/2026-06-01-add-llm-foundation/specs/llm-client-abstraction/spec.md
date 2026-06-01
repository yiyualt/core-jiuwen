## ADDED Requirements

### Requirement: ModelClientConfig
系统 SHALL 提供 `ModelClientConfig` Pydantic model，包含 provider、api_key、api_base、verify_ssl。

#### Scenario: Default construction
- **WHEN** 创建 `ModelClientConfig(provider="openai", api_key="sk-xxx")`
- **THEN** api_base 默认为空，verify_ssl 默认为 True

### Requirement: ModelRequestConfig
系统 SHALL 提供 `ModelRequestConfig` Pydantic model，包含 model、temperature、max_tokens、top_p、stop。

#### Scenario: Default construction
- **WHEN** 创建 `ModelRequestConfig(model="gpt-4")`
- **THEN** temperature=0.7, max_tokens=1024

### Requirement: LLMClient abstract interface
系统 SHALL 提供 `LLMClient` ABC，定义 `chat(messages, config) -> str` 和 `chat_stream(messages, config) -> AsyncIterator[str]`。

#### Scenario: Subclass must implement chat
- **WHEN** 子类未实现 `chat`
- **THEN** 实例化后调用 `chat()` 抛出 `TypeError`
