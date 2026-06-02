## Why

当前 agent.run() 是黑盒 — 无法监听执行过程中的事件。Task Loop 提供事件驱动架构，让外部可以观察 agent 的每一步（工具调用、错误、完成）。

## What Changes

- 新增 `jiuwen/harness/task_loop/` — 事件循环系统
- events: TaskEvent dataclass（type + data + timestamp）
- handler: EventHandler 接口 + 默认实现
- executor: TaskExecutor 包装 agent.run() + 发出事件
- coordinator: LoopCoordinator 管理任务队列 + 事件分发

## Capabilities

### New Capabilities
- `task-loop`: 事件驱动的 agent 执行循环
