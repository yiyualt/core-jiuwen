## ADDED Requirements

### Requirement: Session stores conversation history
`Session` SHALL 存储对话消息列表，支持添加和查询。

#### Scenario: Add and retrieve messages
- **WHEN** 调用 `session.add_message("user", "hello")` 然后 `session.add_message("assistant", "hi")`
- **THEN** `session.get_messages()` 返回两条消息

### Requirement: Agent supports session parameter
`ReActAgent.run()` SHALL 接受可选的 `session` 参数。

#### Scenario: Multi-turn conversation
- **WHEN** 第一轮调用 `agent.run({"query": "I'm Bob"}, session=s)` 完成后
- **THEN** 第二轮调用 `agent.run({"query": "What's my name?"}, session=s)` 能识别用户叫 Bob
