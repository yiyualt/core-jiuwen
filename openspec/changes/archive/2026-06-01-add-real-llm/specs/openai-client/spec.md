## ADDED Requirements

### Requirement: OpenAIClient implements LLMClient
`OpenAIClient` SHALL 实现 `LLMClient` 接口，通过 openai SDK 发起真实的 chat completion 请求。

#### Scenario: Chat returns response content
- **WHEN** 配置有效的 api_key 和 api_base，调用 `chat([{"role": "user", "content": "hi"}])`
- **THEN** 返回模型的实际文本响应

#### Scenario: Chat stream yields tokens
- **WHEN** 调用 `chat_stream(messages)` 
- **THEN** 逐个 yield 模型输出的 token 字符串

### Requirement: from_env factory method
`OpenAIClient.from_env(env_file=None)` SHALL 从 .env 文件读取配置并创建实例。

#### Scenario: Read from .env
- **WHEN** .env 包含 OPENAI_API_KEY=sk-xxx, OPENAI_API_BASE=https://api.example.com
- **THEN** from_env() 返回正确配置的 OpenAIClient

### Requirement: FakeLLMClient removed from source
`FakeLLMClient` SHALL 从 `jiuwen/core/foundation/llm.py` 移除，仅存在于 `tests/conftest.py`。

#### Scenario: Import from tests only
- **WHEN** 在测试中 `from tests.conftest import FakeLLMClient`
- **THEN** 可正常使用预编程响应

### Requirement: LLMComponent defaults to real client
`LLMComponent(config)` 不带 client 参数时 SHALL 使用 `OpenAIClient.from_env()`。

#### Scenario: Default to OpenAIClient
- **WHEN** 已配置 .env，调用 `LLMComponent(config)`
- **THEN** 内部使用 OpenAIClient 实例
