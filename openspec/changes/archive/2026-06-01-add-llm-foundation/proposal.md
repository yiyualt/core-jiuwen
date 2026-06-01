## Why

Workflow 系统已经可以编排组件 pipeline，但缺少实际的 AI 能力。LLM Foundation 提供大模型调用的基础抽象，让后续可以构建 LLMComponent 接入 workflow。

## What Changes

- 新增 `jiuwen/core/foundation/` 模块
- `llm.py`: ModelClientConfig（连接配置）、ModelRequestConfig（请求参数）、LLMClient 抽象基类、FakeLLMClient 测试替身
- 将 tests/conftest.py 中的 FakeLLM 升级为正式的 FakeLLMClient
- 测试、文档

## Capabilities

### New Capabilities
- `llm-client-abstraction`: LLM 调用的配置模型和客户端抽象接口
- `fake-llm-client`: 测试用 FakeLLMClient，返回预编程响应

## Impact

- 新增 `jiuwen/core/foundation/` 包
- 更新 `tests/conftest.py` 使用新的 `FakeLLMClient`
