## Context

Tool 是 ReActAgent 的核心依赖。遵循 Card/Config 分离：ToolCard 描述工具身份，ToolComponent 负责执行。

## Goals / Non-Goals

**Goals:**
- ToolCard 继承 BaseCard，增加 parameters（JSON Schema）和 func（可调用对象）
- ToolComponent 包装 ToolCard，invoke 时根据 inputs 调用 func
- 支持同步和 async 工具函数
- 支持工具注册表（dict 存储）

**Non-Goals:**
- 不实现 LLM 自动工具选择（那是 ReActAgent 的事）
- 不实现远程工具调用（HTTP）

## Decisions

**1. ToolCard 继承 BaseCard**

```python
class ToolCard(BaseCard):
    parameters: dict | None = None  # JSON Schema for parameters
    func: Callable | None = None    # the actual function

    def tool_info(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters or {},
        }
```

**2. ToolComponent 包装 ToolCard**

```python
class ToolComponent(WorkflowComponent):
    def __init__(self, card: ToolCard):
        self._card = card

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        if self._card.func is None:
            raise ValueError(f"Tool '{self._card.name}' has no function")
        result = self._card.func(**inputs)
        if inspect.isawaitable(result):
            result = await result
        return {"output": result}
```

支持同步和 async 工具：
- `def search(q): return ["result1"]` → 同步
- `async def fetch(url): return await http.get(url)` → 异步

**3. 并发执行**

ToolComponent 作为普通 WorkflowComponent，可以在 Workflow 的 PregelGraph 中与其他组件并行。
