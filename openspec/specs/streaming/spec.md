## ADDED Requirements

### Requirement: StreamEmitter
`StreamEmitter` SHALL 提供异步 emit/yield 接口用于流式输出。

#### Scenario: Emit and iterate
- **WHEN** 调用 `emitter.emit("hello")` 和 `emitter.emit(None)`（结束信号）
- **THEN** `async for chunk in emitter:` 依次 yield "hello"

### Requirement: ReActAgent supports streaming
`ReActAgent.stream(inputs)` SHALL 流式产出中间步骤和最终结果。

#### Scenario: Stream yields intermediate steps
- **WHEN** 调用 `agent.stream({"query": "test"})`
- **THEN** yield Thought/Action/Observation/Final Answer 各步骤
