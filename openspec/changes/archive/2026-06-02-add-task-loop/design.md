## Context

将黑盒 agent.run() 包装为可观察的事件流。

## Decisions

**1. TaskEvent**

```python
@dataclass
class TaskEvent:
    type: str          # "task_start", "tool_call", "task_complete", "error"
    data: dict         # payload
    timestamp: float   # time.time()
```

**2. EventHandler**

```python
class EventHandler(ABC):
    async def on_event(self, event: TaskEvent): ...
```

默认实现 `LoggingHandler`：打印到 stdout。

**3. TaskExecutor**

```python
class TaskExecutor:
    def __init__(self, agent, handlers=None):
        ...

    async def execute(self, task: str, session=None) -> dict:
        await self._emit("task_start", {"task": task})
        try:
            result = await self._agent.run({"query": task}, session=session)
            await self._emit("task_complete", {"result": result})
            return result
        except Exception as e:
            await self._emit("error", {"error": str(e)})
            raise
```

**4. LoopCoordinator**

```python
class LoopCoordinator:
    def __init__(self, executor, max_tasks=None):
        self._queue = asyncio.Queue()
        ...

    async def submit(self, task: str, session=None):
        await self._queue.put((task, session))

    async def run(self):
        while True:
            task, session = await self._queue.get()
            if task is None:  # sentinel
                break
            await self._executor.execute(task, session)
```
