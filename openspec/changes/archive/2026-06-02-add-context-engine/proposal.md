## Why

LLM 有上下文窗口限制（如 128K tokens）。长对话会超限。Context Engine 管理消息缓冲：当上下文接近限制时自动裁剪旧消息，保持对话在窗口内。

## What Changes

- 新增 `jiuwen/core/context_engine/` 模块
- `token_counter.py`: 估算 token 数量（基于字符数或 tiktoken）
- `message_buffer.py`: 管理消息列表，自动裁剪
- `model_context.py`: 高层 API，组合 buffer + counter
- Agent 集成：ReActAgent 可选用 ContextEngine 管理长对话

## Capabilities

### New Capabilities
- `context-engine`: 上下文窗口管理（token 计数 + 消息缓冲 + 自动裁剪）
