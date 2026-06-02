## ADDED Requirements

### Requirement: CoordinatorAgent delegates to members
`CoordinatorAgent` SHALL 内置 `delegate` 工具，可调用成员 agent 执行子任务。

#### Scenario: Delegate to member
- **WHEN** Coordinator 执行 `delegate(agent_name="researcher", task="search AI")`
- **THEN** 调用 researcher.run({"query": "search AI"}) 并返回结果

### Requirement: Team orchestrates multiple agents
`Team` SHALL 管理成员注册并通过 Coordinator 协调执行。

#### Scenario: Team completes complex task
- **WHEN** 创建 Team(researcher, writer)，调用 `team.run("Research and write")`
- **THEN** Coordinator 先 delegate 给 researcher，再 delegate 给 writer，返回最终报告

### Requirement: Team works with FakeLLMClient
Coordinator 的 delegating 逻辑 SHALL 可用 FakeLLMClient 完全测试。

#### Scenario: Test with FakeLLMClient
- **WHEN** Coordinator 使用 FakeLLMClient(["Action: delegate(...)", "Final Answer: done"])
- **THEN** 成员 agent 被正确调用，返回预期结果
