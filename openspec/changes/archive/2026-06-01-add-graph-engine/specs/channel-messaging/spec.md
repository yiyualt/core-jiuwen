## ADDED Requirements

### Requirement: Channel abstract base
系统 SHALL 提供 `Channel` 抽象基类，定义 `is_ready`, `accept`, `consume`, `snapshot`, `restore` 方法。

#### Scenario: Channel interface
- **WHEN** 查看 `Channel` 类
- **THEN** 包含属性 `key` 和 `node_name`，以及方法 `is_ready()`, `accept(msg)`, `consume()`, `snapshot()`, `restore(state)`

### Requirement: TriggerChannel OR-gate semantics
`TriggerChannel` SHALL 在收到任意一条消息后变为 ready。

#### Scenario: Becomes ready after first message
- **WHEN** 新建 TriggerChannel，调用 `accept(TriggerMessage)`
- **THEN** `is_ready()` 返回 `True`

#### Scenario: Not ready initially
- **WHEN** 新建 TriggerChannel
- **THEN** `is_ready()` 返回 `False`

#### Scenario: Reset after consume
- **WHEN** TriggerChannel ready 后调用 `consume()`
- **THEN** `is_ready()` 返回 `False`

### Requirement: BarrierChannel AND-gate semantics
`BarrierChannel` SHALL 在**所有**预期 sender 都到达后变为 ready。

#### Scenario: Not ready after partial arrival
- **WHEN** 新建 BarrierChannel(expected={"a", "b"})，只 accept sender="a" 的消息
- **THEN** `is_ready()` 返回 `False`

#### Scenario: Ready after all senders arrive
- **WHEN** 新建 BarrierChannel(expected={"a", "b"})，依次 accept sender="a" 和 sender="b"
- **THEN** `is_ready()` 返回 `True`

#### Scenario: Duplicate sender ignored
- **WHEN** sender="a" 的消息被 accept 两次
- **THEN** 第二次 accept 返回 `False`（状态未变）

#### Scenario: Unknown sender ignored
- **WHEN** BarrierChannel(expected={"a"}) 收到 sender="unknown" 的消息
- **THEN** `is_ready()` 返回 `False`，状态不变

### Requirement: Channel snapshot and restore
Channel SHALL 支持 `snapshot()` 返回可序列化状态，`restore()` 从快照恢复。

#### Scenario: TriggerChannel snapshot
- **WHEN** TriggerChannel 中有两条消息，调用 `snapshot()`
- **THEN** 返回包含两条消息的列表

#### Scenario: BarrierChannel snapshot
- **WHEN** BarrierChannel 收到 {a, b} 中只有 a 到达，调用 `snapshot()`
- **THEN** 返回 `["a"]`
