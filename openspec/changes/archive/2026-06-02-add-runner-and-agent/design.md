## Context

Runner 和 Agent 是 jiuwen 的上层抽象。Runner 是全局单例入口，Agent 是面向用户的智能体接口。

## Goals / Non-Goals

**Goals:**
- Runner 全局单例，resource_mgr 管理注册
- AgentCard 描述智能体身份
- WorkflowAgent 绑定 workflow 并通过 Runner 执行
- 用户代码从 `wf.invoke()` 升级到 `Runner.run_agent(agent, inputs)`

**Non-Goals:**
- 不实现 ReActAgent（留给后续版本）
- 不实现分布式（Runner 但预留扩展点）

## Decisions

**1. Runner 单例模式**

```python
class Runner:
    resource_mgr: ResourceManager = ResourceManager()

    @classmethod
    async def run_agent(cls, agent: "WorkflowAgent", inputs: dict) -> dict:
        return await agent.run(inputs)
```

`Runner.resource_mgr` 是进程级全局状态，类似 agent-core 的设计。

**2. ResourceManager**

```python
class ResourceManager:
    def __init__(self):
        self._workflows: dict[str, Workflow] = {}
        self._tools: dict[str, ToolCard] = {}

    def add_workflow(self, key: str, factory):
        self._workflows[key] = factory

    def get_workflow(self, key: str) -> Workflow:
        ...
```

**3. AgentCard + WorkflowAgentConfig**

```python
class AgentCard(BaseCard):
    version: str = ""
    model: str = ""

class WorkflowAgentConfig(BaseModel):
    id: str = ""
    version: str = ""
    description: str = ""
```

**4. WorkflowAgent**

```python
class WorkflowAgent:
    def __init__(self, config: WorkflowAgentConfig):
        self._config = config
        self._workflows: list[Workflow] = []

    def add_workflows(self, workflows: list[Workflow]):
        self._workflows.extend(workflows)

    async def run(self, inputs: dict) -> dict:
        # Run all workflows, return combined results
        ...
```

**5. 使用方式变化**

```python
# 之前
wf = Workflow()
wf.set_start_comp(...)
result = await wf.invoke({"query": "hello"})

# 之后
agent = WorkflowAgent(config)
agent.add_workflows([wf])
result = await Runner.run_agent(agent, {"query": "hello"})
```

Runner 还支持注册 workflow 供后续复用：
```python
Runner.resource_mgr.add_workflow("my_wf_1.0", lambda: create_my_wf())
```
