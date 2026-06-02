## Context

从教学级 simplify 升级为接近原项目的功能级实现。

## Decisions

**1. InProcessMessager**

```python
class InProcessMessager:
    """Async message passing between agents in the same process."""
    def __init__(self):
        self._queues: dict[str, asyncio.Queue] = {}

    async def send(self, target: str, message: dict):
        queue = self._queues.setdefault(target, asyncio.Queue())
        await queue.put(message)

    async def receive(self, agent_name: str) -> dict:
        queue = self._queues.setdefault(agent_name, asyncio.Queue())
        return await queue.get()
```

**2. Schema**

```python
@dataclass
class TeamEvent:
    type: str  # "task_assigned", "task_complete", "agent_message", "error"
    source: str
    target: str | None
    data: dict

@dataclass 
class TaskBlueprint:
    task_id: str
    description: str
    assigned_to: str | None
    status: str  # "pending", "running", "done", "failed"
    result: dict | None = None
```

**3. Spawner**

```python
class AgentSpawner:
    """Creates child agents with isolated or shared resources."""
    def __init__(self, messager=None):
        self._messager = messager or InProcessMessager()
        self._agents: dict[str, Any] = {}

    def spawn(self, name: str, factory, **kwargs) -> Any:
        agent = factory(**kwargs)
        self._agents[name] = agent
        return agent
```
