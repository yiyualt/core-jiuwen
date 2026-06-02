Context Engine: 上下文窗口管理
=================================

LLM 有上下文窗口限制（如 GPT-4 的 128K tokens）。对话太长会超限。
Context Engine 负责**估算 token 数**并在接近限制时**自动裁剪**旧消息。

核心概念
--------

.. code-block:: text

    MessageBuffer(max_tokens=4096)

    添加消息:                             获取消息:
    ┌─────────────────────┐             ┌─────────────────────┐
    │ System: 你是助手      │             │ System: 你是助手      │  ← 始终保留
    │ User: 第1轮问题       │             │ User: 第98轮问题      │
    │ Assistant: 第1轮回答   │  超过限制   │ Assistant: 第98轮回答  │
    │ User: 第2轮问题       │ ────────→   │ User: 第99轮问题      │
    │ ...                  │  自动裁剪    │ Assistant: 第99轮回答  │
    │ User: 第99轮问题      │             └─────────────────────┘
    │ Assistant: 第99轮回答  │              (旧消息被丢弃，保持窗口内)
    └─────────────────────┘

用法
----

.. code-block:: python

    from jiuwen.core.context_engine import ModelContext

    ctx = ModelContext(max_tokens=4096)
    ctx.add_system("You are a helpful assistant.")
    ctx.add_user("What is Python?")
    ctx.add_assistant("Python is a programming language.")
    ctx.add_user("Tell me more...")

    messages = ctx.get_messages()  # 自动裁剪到 4096 tokens

裁剪策略：system 消息**始终保留**，从最早的 user+assistant 对开始丢弃。
