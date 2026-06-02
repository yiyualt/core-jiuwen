## ADDED Requirements

### Requirement: LoopComponent repeats execution
在 max_iterations 内重复执行，积累数据。

#### Scenario: Loop accumulates items
- **WHEN** 连续 3 次 invoke，每次输入不同的 item
- **THEN** 最终返回 `{"items": [all 3], "done": True}`
