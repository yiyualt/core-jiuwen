## Why

auto_harness 是 agent-core 的"元框架"——用 DeepAgent 自动优化 harness 自身。它定义了标准化的演进管道：评估 → 计划 → 实施 → 验证 → 提交。

## What Changes

- 新增 `jiuwen/auto_harness/` 顶层包
- `orchestrator.py`: 编排演进管道
- `pipeline.py`: PipelineSpec + PipelineRegistry
- `stages.py`: 标准 stage (assess, plan, implement, verify)
- `experience.py`: 经验存储和合成

## Capabilities

### New Capabilities
- `auto-harness`: 自动化 agent 优化框架
