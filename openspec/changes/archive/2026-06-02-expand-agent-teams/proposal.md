## Why

agent_teams 目前只有 1 个文件（Coordinator + Team），缺少原项目的核心子系统。补全 messager（消息传递）、schema（事件/任务）、spawn（子 agent 生成）。

## What Changes

- `agent_teams/messager/`: InProcessMessager — 进程内异步消息传递
- `agent_teams/schema/`: TeamEvent, TaskStatus, TaskBlueprint
- `agent_teams/spawn/`: Spawner — 子 agent 生成 + 共享资源

## Capabilities

### Modified Capabilities
- `agent-teams`: 从 1 文件扩展为完整的多 agent 协作系统
