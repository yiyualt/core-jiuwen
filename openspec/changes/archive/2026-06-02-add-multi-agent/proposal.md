## Why

agent_teams 实现了静态团队（Coordinator + 固定 members）。multi_agent 提供动态的多 agent 运行时：消息总线、任务路由、handoff（交接）。

## What Changes

- 新增 `jiuwen/core/multi_agent/` 模块
- `message_bus.py`: 集中式消息总线，订阅/发布
- `team_runtime.py`: 团队运行时，管理 agent 生命周期
- `handoff.py`: 任务交接 — 一个 agent 把任务转给另一个

## Capabilities

### New Capabilities
- `multi-agent-runtime`: 动态多 agent 运行时和消息总线
