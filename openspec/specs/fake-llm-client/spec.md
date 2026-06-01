## ADDED Requirements

### Requirement: FakeLLMClient returns preprogrammed responses
`FakeLLMClient` SHALL 按顺序返回构造时指定的响应列表，循环复用。

#### Scenario: Returns configured response
- **WHEN** 创建 `FakeLLMClient(["hello"])` 并调用 `chat([...])`
- **THEN** 返回 `"hello"`

#### Scenario: Cycles through responses
- **WHEN** 创建 `FakeLLMClient(["a", "b"])` 并调用 `chat()` 三次
- **THEN** 返回 `"a"`, `"b"`, `"a"`

#### Scenario: Tracks call count
- **WHEN** 调用 `chat()` 两次
- **THEN** `client.call_count == 2`

#### Scenario: Records last messages
- **WHEN** 调用 `chat([{"role": "user", "content": "hi"}])`
- **THEN** `client.last_messages == [{"role": "user", "content": "hi"}]`

#### Scenario: chat_stream yields the same response
- **WHEN** 调用 `chat_stream([...])`
- **THEN** yield 与 `chat()` 相同的结果

### Requirement: conftest fixture compatibility
tests/conftest.py 的 `fake_llm` fixture SHALL 返回 `FakeLLMClient` 实例。

#### Scenario: fixture works
- **WHEN** 测试函数使用 `fake_llm` fixture
- **THEN** 返回 `FakeLLMClient` 实例，可调用 `chat()`
