## Why

Agent 的提示词质量直接影响性能。Agent Evolving 提供自动化的提示词优化：用数据集评估 agent，分析失败案例，迭代改进提示词。

## What Changes

- 新增 `jiuwen/core/agent_evolving/` — Case, Evaluator, Optimizer, Trainer, Checkpoint
- 训练循环: evaluate → analyze failures → generate better prompt → repeat
- 完全可测试（用 FakeLLMClient 模拟评估和优化）

## Capabilities

### New Capabilities
- `agent-evolving`: 自动提示词优化系统
