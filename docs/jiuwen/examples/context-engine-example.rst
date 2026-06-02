Context Engine 示例
====================

基本用法：模拟长对话
---------------------

.. code-block:: python

    from jiuwen.core.context_engine import ModelContext

    # 创建一个 200 token 的窗口
    ctx = ModelContext(max_tokens=200)

    # 添加 system 提示词
    ctx.add_system("You are a helpful Python expert.")

    # 模拟 50 轮对话
    for i in range(50):
        ctx.add_user(f"Question {i}: How do I use list comprehensions? " + "x" * 50)
        ctx.add_assistant(f"Answer {i}: Here is how... " + "y" * 80)

    # 获取消息 — 自动裁剪到 200 tokens
    messages = ctx.get_messages()

    print(f"Total messages: {len(messages)}")
    # 输出: Total messages: 4 或 6
    # system 始终在，但旧的 user+assistant 对被丢弃了

    # 验证 system 消息在
    assert messages[0]["role"] == "system"

裁剪策略演示
-------------

.. code-block:: python

    from jiuwen.core.context_engine import MessageBuffer, TokenCounter

    # 用极小的限制来观察裁剪效果
    counter = TokenCounter()
    buf = MessageBuffer(max_tokens=30, counter=counter)

    buf.add_system("sys")
    buf.add_user("first question here")
    buf.add_assistant("first answer here too")

    # 再添加一对 — 超过限制
    buf.add_user("second question coming")
    buf.add_assistant("second answer back")

    msgs = buf.get_messages()
    print(f"After overflow: {len(msgs)} messages")
    # system + second pair = 3 messages (first pair 被裁剪)

    for m in msgs:
        print(f"  [{m['role']}] {m['content'][:30]}...")

Token 计数
-----------

.. code-block:: python

    from jiuwen.core.context_engine import TokenCounter

    counter = TokenCounter()

    short = [{"role": "user", "content": "hi"}]
    long  = [{"role": "user", "content": "hello world " * 100}]

    print(f"Short: {counter.count(short)} tokens")
    print(f"Long:  {counter.count(long)} tokens")
    # 约 1 vs 25+

集成到 Agent
-------------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.core.single_agent.agents import ReActAgent
    from jiuwen.core.session import Session
    from jiuwen.core.context_engine import ModelContext


    async def main():
        agent = ReActAgent(
            client=FakeLLMClient(["Final Answer: Python is great!"]),
        )
        session = Session()
        ctx = ModelContext(max_tokens=500)

        # 模拟多轮对话
        for i in range(20):
            query = f"Question {i}: " + "tell me more " * 5
            session.add_message("user", query)
            ctx.add_system("You are helpful.")
            ctx.add_messages(session.get_messages())

            result = await agent.run({"query": query}, session=session)
            print(f"Round {i}: {len(ctx.get_messages())} msgs in context")

    asyncio.run(main())
