## ADDED Requirements

### Requirement: InProcessMessager passes messages between agents
`InProcessMessager` SHALL 提供 send/receive 异步消息传递。

#### Scenario: Send and receive
- **WHEN** A send("B", {"msg": "hello"}) 然后 B receive("B")
- **THEN** B 收到 {"msg": "hello"}

### Requirement: TeamEvent and TaskBlueprint define team state
`TeamEvent` 和 `TaskBlueprint` SHALL 提供结构化的团队状态表示。

#### Scenario: Task lifecycle
- **WHEN** 创建 TaskBlueprint(task_id="t1", status="pending")
- **THEN** assigned_to 为 None, result 为 None

### Requirement: AgentSpawner creates child agents
`AgentSpawner.spawn(name, factory)` SHALL 创建并注册 agent。

#### Scenario: Spawn agent
- **WHEN** spawn("coder", lambda: ReActAgent(...))
- **THEN** spawner._agents["coder"] 包含创建的 agent
