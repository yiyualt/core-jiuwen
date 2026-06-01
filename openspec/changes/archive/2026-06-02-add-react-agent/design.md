## Context

ReAct (Reasoning + Acting) 是经典的 LLM Agent 范式。智能体在循环中：思考 → 行动 → 观察 → 重复，直到得出最终答案。

## Goals / Non-Goals

**Goals:**
- ReActAgent 实现 Thought/Action/Observation 循环
- 工具自动发现和调用
- 与 FakeLLMClient 配合可完全测试

**Non-Goals:**
- 不支持流式输出

## Decisions

**1. ReActAgent 设计**

```python
class ReActAgent:
    def __init__(self, client, tools=None, system_prompt="", max_iterations=10):
        ...

    async def run(self, inputs: dict) -> dict:
        history = self._build_initial_messages(inputs)
        for _ in range(self.max_iterations):
            response = await self._client.chat(history)
            parsed = self._parse_output(response)
            if parsed["type"] == "final":
                return {"result": parsed["answer"]}
            elif parsed["type"] == "action":
                observation = await self._execute_action(parsed)
                history.append({"role": "assistant", "content": response})
                history.append({"role": "user", "content": f"Observation: {observation}"})
        return {"result": "Max iterations reached"}
```

**2. Prompt 格式**

```
You are {{system_prompt}}

You have access to these tools:
- {{name}}({{params}}): {{description}}

Use this format:
Thought: your reasoning
Action: tool_name(arg1=val1, arg2=val2)
Observation: tool result
... (repeat as needed)
Thought: I now know the answer
Final Answer: the final response

User's question: {{query}}
```

**3. 输出解析**

用正则提取 Thought、Action、Final Answer：

```python
def _parse_output(self, text):
    if "Final Answer:" in text:
        return {"type": "final", "answer": text.split("Final Answer:")[-1].strip()}
    action_match = re.search(r"Action:\s*(.+)", text)
    if action_match:
        return {"type": "action", "action": action_match.group(1).strip()}
    return {"type": "unknown", "text": text}
```

**4. 工具执行**

```python
async def _execute_action(self, parsed):
    tool_name, args = parse_tool_call(parsed["action"])  # "search(query='x')" -> ("search", {"query": "x"})
    tool = self._tools[tool_name]
    comp = ToolComponent(tool)
    result = await comp.invoke(args)
    return str(result["output"])
```
