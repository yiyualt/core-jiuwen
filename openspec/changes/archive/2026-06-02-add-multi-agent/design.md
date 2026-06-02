## Context

agent_teams 是静态的（预定义成员）。multi_agent 是动态的（运行时注册、发现、交接）。

## Decisions

**1. MessageBus**

```python
class MessageBus:
    """Publish-subscribe message bus for agents."""
    def __init__(self):
        self._subscribers: dict[str, list[callable]] = {}

    def subscribe(self, topic: str, handler): ...
    async def publish(self, topic: str, message: dict): ...
```

**2. TeamRuntime**

```python
class TeamRuntime:
    """Manages agent lifecycle and task routing."""
    def __init__(self, bus=None):
        self._bus = bus or MessageBus()
        self._agents: dict[str, Any] = {}

    def register(self, name: str, agent, capabilities: list[str]): ...
    def route(self, task: str) -> str:  # Find best agent for task
        ...
```

**3. Handoff**

```python
async def handoff(source_agent, target_agent, task, session=None):
    """Transfer a task from one agent to another."""
    ...
```
