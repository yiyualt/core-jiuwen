## Context

拥有 FakeLLMClient 后，可以构建 LLMComponent 了。设计目标：最小化但可用。

## Goals / Non-Goals

**Goals:**
- LLMCompConfig：封装 client_config + model_config + template_content + output_config
- LLMComponent：接收 LLMClient，渲染提示词模板，调用 LLM，返回结构化输出
- 端到端：Start → LLM → End 的完整 pipeline

**Non-Goals:**
- 不实现 OpenAI/真实 provider
- 不支持流式（chat_stream 已就绪但 v0.0.5 只用 chat）

## Decisions

**1. LLMCompConfig 结构**

```python
class LLMCompConfig(BaseModel):
    model_client_config: ModelClientConfig
    model_config: ModelRequestConfig
    template_content: list[dict]  # 消息模板列表
    output_config: dict | None    # 期望的输出 JSON Schema
```

**2. 模板渲染**

复用 End 组件的 `{{var}}` → `$var` 模式，在 invoke 时将模板中的占位符替换为实际输入值：

```python
template = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "{{query}}"},
]
# 输入 {"query": "你好"} → 消息 [{"role": "user", "content": "你好"}]
```

**3. LLMComponent 实现**

```python
class LLMComponent(WorkflowComponent):
    def __init__(self, config: LLMCompConfig, client: LLMClient | None = None):
        self._config = config
        self._client = client or FakeLLMClient()

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        messages = self._render_template(inputs)
        response = await self._client.chat(messages, self._config.model_config)
        return self._parse_response(response)
```

**4. FakeLLMClient 作为默认客户端**

如果未提供 client，使用 FakeLLMClient(["default response"])。测试中注入 FakeLLMClient 设置预期响应。
