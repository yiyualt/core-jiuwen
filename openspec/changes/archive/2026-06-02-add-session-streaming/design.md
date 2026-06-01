## Context

Session 让 agent 拥有记忆，StreamEmitter 让输出实时可见。

## Goals / Non-Goals

**Goals:**
- Session 管理对话历史 (messages list)
- StreamEmitter 提供 yield 接口
- Agent 和 Runner 支持 session 参数

**Non-Goals:**
- 不实现持久化（会话不存盘）
- 不实现 interrupt/resume

## Decisions

**1. Session 设计**

```python
class Session:
    def __init__(self):
        self._messages: list[dict] = []
        self._state: dict = {}

    def add_message(self, role: str, content: str):
        self._messages.append({"role": role, "content": content})

    def get_messages(self) -> list[dict]:
        return list(self._messages)
```

**2. StreamEmitter**

```python
class StreamEmitter:
    def __init__(self):
        self._queue = asyncio.Queue()

    async def emit(self, chunk):
        await self._queue.put(chunk)

    async def __aiter__(self):
        while True:
            chunk = await self._queue.get()
            if chunk is None:  # sentinel
                break
            yield chunk
```

**3. Agent.run() 签名变化**

```python
# 之前
async def run(self, inputs: dict) -> dict

# 之后
async def run(self, inputs: dict, session: Session | None = None) -> dict
```

有 session 时，agent 把对话历史加入 prompt。结束后把用户问题+回复写入 session。

**4. Runner.run_agent() 签名对齐**

```python
async def run_agent(cls, agent, inputs, session=None) -> dict
```

**5. ReActAgent.stream() 方法**

```python
async def stream(self, inputs, session=None):
    async for chunk in self._run_loop_streaming(inputs, session):
        yield chunk
```
