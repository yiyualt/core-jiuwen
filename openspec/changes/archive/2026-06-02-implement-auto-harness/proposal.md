## Why

auto_harness 当前只有简单的循环执行，缺乏原项目的核心特性：管道注册/发现、流式执行、阶段失败重试、会话上下文。

## What Changes

- 重写 `jiuwen/auto_harness/` — 接近原项目的功能级实现
- 新增 `registry.py`: PipelineRegistry + StageRegistry（注册/查找）
- 新增 `contexts.py`: SessionContext（会话级别共享状态）
- 重写 `pipeline.py`: BasePipeline + StandardPipeline + ExtendedPipeline
- 重写 `orchestrator.py`: 流式执行 + 管道选择 + fix loop
- 新增 `fix_loop.py`: 失败阶段自动重试

## Capabilities

### Modified Capabilities
- `auto-harness`: 从简单循环升级为完整的管道编排框架
