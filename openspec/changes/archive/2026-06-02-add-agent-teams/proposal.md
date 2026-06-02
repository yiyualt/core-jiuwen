## Why

单个 ReActAgent 能力有限。Multi-Agent Teams 让多个专业 agent 协同工作：Coordinator 分解任务，委派给成员 agent 执行，汇总结果。

## What Changes

- 新增 `jiuwen/core/agent_teams/` — Team + CoordinatorAgent
- CoordinatorAgent 继承 ReActAgent，内置 delegate 工具
- Team 管理成员注册和协调执行
- 测试使用 FakeLLMClient 模拟多 agent 交互

## Capabilities

### New Capabilities
- `agent-teams`: 多 agent 协作系统，Coordinator 委派任务给成员 agent
