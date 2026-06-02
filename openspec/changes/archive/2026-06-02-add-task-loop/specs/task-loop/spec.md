## ADDED Requirements

### Requirement: TaskEvent carries execution events
`TaskEvent` SHALL 包含 type, data, timestamp 字段。

#### Scenario: Event creation
- **WHEN** 创建 `TaskEvent(type="task_start", data={"task": "fix bug"})`
- **THEN** timestamp 自动设置为当前时间

### Requirement: EventHandler receives events
`EventHandler.on_event(event)` SHALL 在每次事件发生时被调用。

#### Scenario: Handler called on execute
- **WHEN** 创建带 LoggingHandler 的 TaskExecutor，执行任务
- **THEN** handler.on_event 被调用至少两次（start + complete）

### Requirement: LoopCoordinator queues tasks
`LoopCoordinator` SHALL 管理异步任务队列，顺序执行。

#### Scenario: Submit and execute
- **WHEN** 提交两个任务到 coordinator，调用 coordinator.run()
- **THEN** 两个任务按顺序执行
