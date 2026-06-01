## Why

v0.0.4 提供了 LLMClient 抽象和 FakeLLMClient，现在是时候把它们接入 Workflow。LLMComponent 让 Workflow pipeline 拥有 AI 能力，实现第一个真正有意义的端到端示例：Start → LLM → End。

## What Changes

- 新增 `jiuwen/core/workflow/components/llm/` 模块
- `llm_comp.py`: LLMCompConfig（配置模型）+ LLMComponent（WorkflowComponent 子类）
- 支持模板化提示词构建：`{{变量}}` 语法在 invoke 时动态填充
- 测试使用 FakeLLMClient，无需真实 API
- 文档

## Capabilities

### New Capabilities
- `llm-component`: LLM as a WorkflowComponent，支持模板提示词和流式输出

## Impact

- 新增 `jiuwen/core/workflow/components/llm/` 包
- 新增对应测试和文档
- 更新 `jiuwen/core/workflow/components/__init__.py` 导出
