## Context

管理 LLM 上下文窗口：估算 token 数，裁剪超限消息。

## Decisions

**1. TokenCounter**

```python
class TokenCounter:
    def __init__(self, model="gpt-4"):
        self._model = model

    def count(self, messages: list[dict]) -> int:
        # 简化：字符数 / 4（英文约 4 字符/token）
        total = 0
        for msg in messages:
            total += len(msg.get("content", ""))
        return total // 4
```

**2. MessageBuffer**

```python
class MessageBuffer:
    def __init__(self, max_tokens=4096, counter=None):
        self._max = max_tokens
        self._counter = counter or TokenCounter()
        self._messages: list[dict] = []

    def add(self, role, content): ...
    def get_messages(self) -> list[dict]:
        # 返回裁剪后的消息（保留 system + 最近的 user/assistant）
        ...
```

**3. ModelContext**

```python
class ModelContext:
    def __init__(self, max_tokens=4096):
        self._buffer = MessageBuffer(max_tokens)

    def add_system(self, content): ...
    def add_user(self, content): ...
    def add_assistant(self, content): ...
    def get_messages(self) -> list[dict]: ...
```

高层 API：`add_*` 添加消息，`get_messages()` 返回裁剪后的。
