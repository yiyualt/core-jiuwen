## Context

从纯测试替身升级为真实 LLM 调用能力。

## Goals / Non-Goals

**Goals:**
- OpenAIClient 实现 LLMClient 接口
- from_env() 工厂方法
- LLMComponent 开箱即用（只需配置 .env）

**Non-Goals:**
- 不实现 Anthropic/其他 provider
- 测试不依赖真实 LLM

## Decisions

**1. OpenAIClient 实现**

```python
class OpenAIClient(LLMClient):
    def __init__(self, client_config: ModelClientConfig):
        self._config = client_config
        self._client = openai.AsyncOpenAI(
            api_key=client_config.api_key,
            base_url=client_config.api_base or None,
        )

    async def chat(self, messages, config=None) -> str:
        cfg = config or ModelRequestConfig()
        response = await self._client.chat.completions.create(
            model=cfg.model,
            messages=messages,
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
            top_p=cfg.top_p,
            stop=cfg.stop,
        )
        return response.choices[0].message.content or ""

    async def chat_stream(self, messages, config=None):
        cfg = config or ModelRequestConfig()
        stream = await self._client.chat.completions.create(
            model=cfg.model, messages=messages, stream=True, ...
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

**2. from_env() 工厂**

```python
@classmethod
def from_env(cls, env_file: str | None = None):
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()
    return cls(ModelClientConfig(
        provider=os.getenv("OPENAI_PROVIDER", "openai"),
        api_key=os.getenv("OPENAI_API_KEY", ""),
        api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
    ))
```

**3. FakeLLMClient 迁移**

从 `jiuwen/core/foundation/llm.py` 移到 `tests/conftest.py`。测试不需要真实 LLM。

**4. LLMComponent 默认值**

```python
# 之前
self._client = client or FakeLLMClient()

# 之后
self._client = client or OpenAIClient.from_env()
```

如果 .env 未配置，OpenAIClient 会因 api_key 为空而报错 — 这比静默回退更好，用户会立即知道需要配置。

## Risks

- 用户没有配置 .env 时 LLMComponent() 会报错 → 用清晰的错误信息引导
- openai SDK 是可选依赖？→ 加入 core dependencies
