## ADDED Requirements

### Requirement: AgentCard extends BaseCard
`AgentCard` SHALL 继承 `BaseCard`，增加 `version` 和 `model` 字段。

#### Scenario: AgentCard construction
- **WHEN** 创建 `AgentCard(id="a1", name="assistant", version="0.1", model="gpt-4o")`
- **THEN** 所有字段正确赋值

### Requirement: WorkflowAgent
`WorkflowAgent` SHALL 绑定一个或多个 Workflow，通过 `run(inputs)` 执行。

#### Scenario: Run single workflow
- **WHEN** agent 绑定一个 workflow，调用 `await agent.run({"query": "hello"})`
- **THEN** 返回 `{"result": ...}` 格式的结果

#### Scenario: Register workflows via Runner
- **WHEN** 通过 `Runner.resource_mgr.add_workflow()` 注册，agent 绑定该 workflow
- **THEN** Runner.run_agent() 正确执行
