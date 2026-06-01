## ADDED Requirements

### Requirement: Super-step execution loop
`CompiledGraph` SHALL 以 super-step 循环执行节点：每步找出就绪节点、并发执行、路由输出到下游 channel。

#### Scenario: Single node graph execution
- **WHEN** 图只有一个节点 "a"（标记为 start 和 end），调用 `_invoke({"value": 5})`
- **THEN** 节点 "a" 被正确执行，结果包含在输出中

#### Scenario: Two-node linear execution
- **WHEN** 图有 start→"a"→"b"→end，调用 `_invoke(data)`
- **THEN** "a" 先执行，输出路由到 "b"，"b" 再执行

#### Scenario: Multiple start nodes execute concurrently
- **WHEN** 图有两个 start 节点 "a" 和 "b"（无依赖关系），调用 `_invoke(data)`
- **THEN** 两个节点都以 data 作为输入执行

### Requirement: Recursion limit
`CompiledGraph` SHALL 限制最大执行步数为 100，防止无限循环。

#### Scenario: Max step limit
- **WHEN** `MAX_RECURSIVE_LIMIT` 被定义
- **THEN** 其值为 100

### Requirement: Output routing via adjacency
节点执行后 SHALL 将输出路由到相邻下游节点的 channel。

#### Scenario: Output routes to downstream
- **WHEN** 边 a→b 存在，节点 "a" 执行完成
- **THEN** 节点 "b" 的 channel 收到 TriggerMessage

#### Scenario: End node output collected
- **WHEN** end 节点执行完成
- **THEN** 其输出被收集到最终结果字典中

### Requirement: Error propagation
节点执行中的异常 SHALL 向上传播，终止整个图的执行。

#### Scenario: Failing node propagates error
- **WHEN** start 节点抛出 `NotImplementedError`
- **THEN** `_invoke()` 抛出 `NotImplementedError`
