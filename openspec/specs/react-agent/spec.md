## ADDED Requirements

### Requirement: ReActAgent construction
`ReActAgent` SHALL 接收 LLMClient、工具列表、system_prompt 和 max_iterations。

#### Scenario: Default construction
- **WHEN** 创建 `ReActAgent(client, tools=[...])`
- **THEN** system_prompt 为空，max_iterations=10

### Requirement: ReAct prompt building
`ReActAgent` SHALL 构建包含工具描述和格式指令的系统提示词。

#### Scenario: Prompt includes tool descriptions
- **WHEN** tools 包含 ToolCard(name="search", description="Search web", parameters={"q": "string"})
- **THEN** 生成的 prompt 包含 "search(q): Search web" 描述

### Requirement: Output parsing
`ReActAgent` SHALL 解析 LLM 输出中的 Final Answer 和 Action。

#### Scenario: Parse final answer
- **WHEN** LLM 返回 "Thought: I know\nFinal Answer: 42"
- **THEN** 解析为 `{"type": "final", "answer": "42"}`

#### Scenario: Parse action
- **WHEN** LLM 返回 "Thought: need to search\nAction: search(q='hello')"
- **THEN** 解析为 `{"type": "action", "action": "search(q='hello')"}`

### Requirement: Tool execution
`ReActAgent` SHALL 根据解析的 Action 调用对应的工具。

#### Scenario: Execute tool
- **WHEN** Action 为 "add(a=3, b=4)"，tools 中有 add 工具
- **THEN** 调用 add(3, 4)，返回 Observation 字符串

### Requirement: ReAct loop
`ReActAgent.run()` SHALL 执行 Thought→Action→Observation 循环直到 Final Answer 或达到 max_iterations。

#### Scenario: Complete loop with FakeLLMClient
- **WHEN** FakeLLMClient 先返回 Action 再返回 Final Answer
- **THEN** run() 返回最终答案
