## Context

Coordinator 是特化的 ReActAgent，`delegate` 工具调用成员 agent。

## Decisions

**1. CoordinatorAgent**

```python
class CoordinatorAgent(ReActAgent):
    def __init__(self, client, members=None, system_prompt="", max_iterations=10):
        def delegate(agent_name: str, task: str) -> str:
            member = members[agent_name]
            result = await member.run({"query": task})  # run synchronously in event loop
            return result["result"]

        delegate_tool = ToolCard(name="delegate", func=delegate, ...)
        super().__init__(client=client, tools=[delegate_tool], ...)
```

**2. Team**

```python
class Team:
    def __init__(self, members, client=None):
        self._members = members
        self._client = client or OpenAIClient.from_env()
        self._coordinator = CoordinatorAgent(
            client=self._client,
            members=self._members,
            system_prompt="You coordinate a team...",
        )

    async def run(self, task: str) -> dict:
        return await self._coordinator.run({"query": task})
```

**3. 用法**

```python
researcher = ReActAgent(client, tools=[search_tool])
writer = ReActAgent(client, tools=[])

team = Team(members={"researcher": researcher, "writer": writer})
result = await team.run("Research AI safety and write a report")
```

**4. 测试**

用 FakeLLMClient 模拟 Coordinator 的多轮行为：先 delegate 给 researcher，再 delegate 给 writer，最后输出 Final Answer。
