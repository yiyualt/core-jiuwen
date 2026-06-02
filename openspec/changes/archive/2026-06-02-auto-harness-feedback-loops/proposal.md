## Why

当前 auto_harness 只是静态管道，缺少原项目的核心"auto"能力：失败自动修复、经验积累学习、会话级编排。

## What Changes

- 升级 `FixLoopController`: error injection + evaluator
- 升级 `ExperienceStore`: 文件持久化 + 关键词搜索 + 时间衰减合成
- 新增 `learnings_stage.py`: 会话结束后反思总结
- 新增 `session_pipeline.py`: MetaEvolvePipeline (assess→plan→per-task→learnings)
- 升级 `Orchestrator`: 支持会话级管道

## Capabilities

### Modified Capabilities
- `auto-harness`: 从静态管道升级为三循环自动优化系统
