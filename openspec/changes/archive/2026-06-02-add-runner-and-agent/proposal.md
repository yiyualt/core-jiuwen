## Why

Workflow 可以直接 invoke，但缺少统一的**入口层**和**智能体抽象**。Runner 提供全局注册表和统一执行入口，Agent 提供面向用户的接口（`agent.run()`），让 jiuwen 从"组件框架"升级为"智能体 SDK"。

## What Changes

- 新增 `jiuwen/core/runner/` — Runner + resource_mgr
- 新增 `jiuwen/core/single_agent/` — AgentCard + WorkflowAgent + WorkflowAgentConfig
- Runner.resource_mgr 管理 workflow、tool、agent 注册
- Runner.run_agent() 统一执行入口
- 文档和测试

## Capabilities

### New Capabilities
- `runner`: 全局执行入口，资源注册中心
- `workflow-agent`: 绑定工作流的智能体抽象

## Impact

- 新增 `jiuwen/core/runner/` 包
- 新增 `jiuwen/core/single_agent/` 包
- 新增对应测试和文档
