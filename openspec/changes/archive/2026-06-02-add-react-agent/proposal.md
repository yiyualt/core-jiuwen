## Why

目前只有 WorkflowAgent（静态流程），缺少动态推理能力。ReActAgent 让智能体能自主选择工具、多轮推理，是 jiuwen 从"工具集"升级为"智能体框架"的关键一步。

## What Changes

- 新增 `jiuwen/core/single_agent/agents/react_agent.py` — ReActAgent 实现
- ReAct 循环: Thought → Action → Observation → repeat
- Prompt 构建: system prompt + 工具描述 + ReAct 格式指令
- LLM 输出解析: 提取 Thought / Action / Final Answer
- 工具调用: 匹配 Action 到 ToolCard，执行 ToolComponent
- 最大循环次数限制，防止死循环

## Capabilities

### New Capabilities
- `react-agent`: 基于 ReAct 范式的智能体，支持工具调用和多轮推理

## Impact

- 新增 `jiuwen/core/single_agent/agents/` 包
- 新增对应测试和文档
