## Context

v0.0.1-3 建立了 Card→Graph→Workflow 的架构。现在是引入 LLM 能力的时机。

## Goals / Non-Goals

**Goals:**
- ModelClientConfig + ModelRequestConfig（Pydantic models）
- LLMClient ABC（chat + chat_stream）
- FakeLLMClient（测试用）

**Non-Goals:**
- 不实现 OpenAI/其他 provider（留给 v0.0.6 LLMComponent）

## Decisions

**1. 两个 Config 分离**

```
ModelClientConfig          ModelRequestConfig
─────────────────         ──────────────────
provider: str              model: str
api_key: str               temperature: float
api_base: str              max_tokens: int
verify_ssl: bool           top_p: float
                           stop: list[str] | None
```

**2. LLMClient 接口**

```python
class LLMClient(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], config: ModelRequestConfig) -> str: ...
    @abstractmethod
    async def chat_stream(self, messages: list[dict], config: ModelRequestConfig) -> AsyncIterator[str]: ...
```

**3. FakeLLMClient — 升级现有测试替身**

```python
class FakeLLMClient(LLMClient):
    def __init__(self, responses: list[str] | None = None):
        self.responses = responses or ["default"]
        self.call_count = 0
        self.last_messages: list[dict] = []

    async def chat(self, messages, config=None) -> str:
        self.last_messages = messages
        r = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return r

    async def chat_stream(self, messages, config=None) -> AsyncIterator[str]:
        text = await self.chat(messages, config)
        yield text
```

更新 tests/conftest.py 的 fake_llm fixture 使用新导入。
