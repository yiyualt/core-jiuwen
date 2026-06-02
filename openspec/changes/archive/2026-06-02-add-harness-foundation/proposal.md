## Why

agent-core 的 `harness/` 是核心用户界面层 — 基于 core primitives 构建的 coding agent 框架。第一期先搭建骨架：DeepAgent、配置、Workspace、工厂函数。

## What Changes

- 新增 `jiuwen/harness/` — 顶层 harness 包
- `deep_agent.py`: DeepAgent 类（继承 ReActAgent，集成编码工具和提示词）
- `schema/config.py`: DeepAgentConfig 配置模型
- `factory.py`: create_deep_agent() 工厂函数
- `workspace/`: Workspace 文件树管理

## Capabilities

### New Capabilities
- `harness-foundation`: coding agent 框架基础（DeepAgent + Workspace + 工厂）

## Impact

- 新增 `jiuwen/harness/` 包（与 `jiuwen/core/` 平级）
- 新增测试和文档
