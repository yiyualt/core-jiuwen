## ADDED Requirements

### Requirement: ToolComponent wraps a ToolCard
`ToolComponent` SHALL 接收 `ToolCard`，在 invoke 时根据 inputs 调用 card.func。

#### Scenario: Invoke synchronous function
- **WHEN** ToolCard 的 func 是同步函数 `def add(a, b): return a + b`，调用 invoke({"a": 3, "b": 4})
- **THEN** 返回 `{"output": 7}`

#### Scenario: Invoke async function
- **WHEN** ToolCard 的 func 是 `async def fetch(x): return "got " + x`，调用 invoke({"x": "data"})
- **THEN** 返回 `{"output": "got data"}`

#### Scenario: No function raises error
- **WHEN** ToolCard 的 func 为 None，调用 invoke
- **THEN** 抛出 ValueError

### Requirement: ToolComponent in workflow pipeline
ToolComponent SHALL 可作为 workflow 节点使用。

#### Scenario: End-to-end pipeline
- **WHEN** workflow: Start → ToolComponent(adder) → End
- **THEN** 正确执行，返回计算结果
