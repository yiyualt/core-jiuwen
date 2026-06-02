## ADDED Requirements

### Requirement: TokenCounter estimates token count
`TokenCounter.count(messages)` SHALL 返回消息列表的估算 token 数。

#### Scenario: Count messages
- **WHEN** 传入 `[{"content": "hello world"}]`
- **THEN** 返回约 2-3（字符数/4）

### Requirement: MessageBuffer trims on overflow
`MessageBuffer` SHALL 在超过 max_tokens 时自动裁剪旧消息，保留 system 消息。

#### Scenario: Trim old messages
- **WHEN** 添加多条消息超过限制
- **THEN** get_messages() 返回的列表在 token 限制内，system 消息始终保留

### Requirement: ModelContext high-level API
`ModelContext` SHALL 提供 add_system/add_user/add_assistant 和 get_messages。

#### Scenario: Build conversation
- **WHEN** 依次调用 add_system, add_user, add_assistant
- **THEN** get_messages() 返回完整的消息历史（未超限时）
