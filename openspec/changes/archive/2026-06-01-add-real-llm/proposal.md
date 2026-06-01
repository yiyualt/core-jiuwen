## Why

当前 `LLMClient` 只有 `FakeLLMClient` 测试替身，无法真正调用大模型。需要实现真实的 OpenAI 兼容客户端，让 jiuwen 具备实际 AI 能力。

## What Changes

- 新增 `OpenAIClient(LLMClient)` — 基于 openai SDK 的真实实现
- `OpenAIClient.from_env()` — 从 .env 自动读取配置
- **BREAKING**: `FakeLLMClient` 从 `jiuwen/core/foundation/llm.py` 移除，下沉到 `tests/conftest.py`
- `LLMComponent` 默认使用 `OpenAIClient.from_env()` 而非 `FakeLLMClient`
- 添加 `openai` 和 `python-dotenv` 依赖
- 创建 `.env.example` 模板
- 更新所有文档和示例使用真实 LLM

## Capabilities

### New Capabilities
- `openai-client`: 基于 OpenAI SDK 的真实 LLM 客户端实现

### Modified Capabilities
- `llm-client-abstraction`: FakeLLMClient 移除，仅测试中存在
- `llm-component`: 默认 client 改为 OpenAIClient.from_env()

## Impact

- `jiuwen/core/foundation/llm.py` — 新增 OpenAIClient，移除 FakeLLMClient
- `jiuwen/core/workflow/components/llm/llm_comp.py` — 改默认 client
- `tests/conftest.py` — 接管 FakeLLMClient
- `docs/` — 全部 LLM 相关文档改为真实调用
- `pyproject.toml` — 加依赖
