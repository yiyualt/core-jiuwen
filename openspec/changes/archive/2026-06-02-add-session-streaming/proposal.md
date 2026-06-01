## Why

当前 agent.run() 每次调用都是独立的，无对话记忆。Session 提供多轮对话能力，StreamEmitter 让 agent 输出可以实时流式返回。

## What Changes

- 新增 `jiuwen/core/session/` — Session + StreamEmitter
- Session 管理对话历史、状态存储
- StreamEmitter 支持流式输出
- Runner.run_agent() 支持 session 参数
- Agent.run() 支持 session 参数（多轮对话）

## Capabilities

### New Capabilities
- `session-management`: 对话历史存储和状态管理
- `streaming`: 流式输出能力

## Impact

- 新增 `jiuwen/core/session/` 包
- 更新 Agent 和 Runner 支持 session
- 新增测试和文档
