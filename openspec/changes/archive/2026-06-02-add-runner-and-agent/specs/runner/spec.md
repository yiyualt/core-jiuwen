## ADDED Requirements

### Requirement: Runner singleton
`Runner` SHALL 作为全局单例，提供 `run_agent()` 类方法作为统一执行入口。

#### Scenario: Run agent
- **WHEN** 调用 `await Runner.run_agent(agent, inputs)`
- **THEN** 委托 agent.run(inputs) 并返回结果

### Requirement: ResourceManager
`Runner.resource_mgr` SHALL 提供 workflow、tool 的注册和查询。

#### Scenario: Register and retrieve workflow
- **WHEN** 调用 `Runner.resource_mgr.add_workflow("key", factory)`
- **THEN** 后续 `get_workflow("key")` 调用 factory 返回 Workflow 实例
