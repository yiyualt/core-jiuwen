## Why

Agent 目前直接执行 LLM 调用和工具调用，没有安全控制层。Rails 系统提供可组合的中间件，在 agent 执行前后拦截、检查、修改输入输出。

## What Changes

- 新增 `jiuwen/core/rails/` — BaseRail + RailPipeline
- 新增 `jiuwen/core/rails/security_rail.py` — 危险操作检测
- RailPipeline 集成到 Runner.run_agent()
- 测试 + 文档

## Capabilities

### New Capabilities
- `rails-system`: 可组合的 agent 中间件管道
