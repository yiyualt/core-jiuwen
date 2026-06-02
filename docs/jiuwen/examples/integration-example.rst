完整集成示例
=============

这个示例把多个模块组合成一个**有安全防护、可观察、有记忆**的 coding agent。
用 FakeLLMClient 完全可运行，不需要真实 API。

.. code-block:: python

    import asyncio
    import tempfile
    from pathlib import Path

    from tests.conftest import FakeLLMClient
    from jiuwen.core.rails import RailPipeline, SecurityRail
    from jiuwen.core.runner import Runner
    from jiuwen.core.session import Session
    from jiuwen.core.context_engine import ModelContext
    from jiuwen.harness import DeepAgent, DeepAgentConfig
    from jiuwen.harness.task_loop import TaskExecutor, LoggingHandler


    async def main():
        # ═══════════════════════════════════════════════
        # 1. 创建安全的工作环境
        # ═══════════════════════════════════════════════
        with tempfile.TemporaryDirectory() as tmp:
            # Workspace: agent 只能操作这个目录
            workspace_dir = tmp

            # ═══════════════════════════════════════════════
            # 2. 配置安全防护 (Rails + Security)
            # ═══════════════════════════════════════════════
            Runner.rails = RailPipeline([
                SecurityRail(),  # 拦截危险命令
            ])

            # ═══════════════════════════════════════════════
            # 3. 创建 Agent (Harness)
            # ═══════════════════════════════════════════════
            client = FakeLLMClient([
                # Agent 会用工具创建文件
                "Action: write(path='hello.py', content='print(42)')",
                "Final Answer: I created hello.py for you.",
            ])
            agent = DeepAgent(
                client,
                DeepAgentConfig(workspace_dir=workspace_dir),
            )

            # ═══════════════════════════════════════════════
            # 4. 多轮对话 (Session + Context Engine)
            # ═══════════════════════════════════════════════
            session = Session()
            ctx = ModelContext(max_tokens=2000)

            queries = [
                "Create hello.py that prints 42",
                "What files do I have?",
                "Run hello.py and show the output",
            ]

            for query in queries:
                session.add_message("user", query)
                ctx.add_user(query)

                # 检查上下文是否超限，自动裁剪
                msgs = ctx.get_messages()
                print(f"[Context: {len(msgs)} messages]")

                # ═══════════════════════════════════════════════
                # 5. 可观察执行 (Task Loop)
                # ═══════════════════════════════════════════════
                executor = TaskExecutor(agent, handlers=[LoggingHandler()])
                result = await executor.execute(query, session=session)

                ctx.add_assistant(str(result.get("result", "")))
                print(f"Agent: {result['result'][:100]}...")
                print()

        # ═══════════════════════════════════════════════
        # 6. 安全输入检查 (独立的 Security 工具)
        # ═══════════════════════════════════════════════
        from jiuwen.core.security import InputGuard

        dangerous = "Please rm -rf /tmp/cache"
        ok, reason = InputGuard.check(dangerous)
        print(f"Safe: {ok}, Reason: {reason}")
        # Safe: False, Reason: Blocked: 'rm -rf'


    asyncio.run(main())

输出示例::

    [Context: 1 messages]
    [task_start] {'task': 'Create hello.py that prints 42'}
    [task_complete] {'result': 'I created hello.py for you.'}
    Agent: I created hello.py for you....

    [Context: 2 messages]
    [task_start] {'task': 'What files do I have?'}
    ...

    Safe: False, Reason: Blocked: 'rm -rf'

这个示例同时用了 6 个模块：

.. list-table::
   :header-rows: 1

   * - 模块
     - 作用
   * - Runner.rails (SecurityRail)
     - 所有 agent 调用自动检查输入
   * - DeepAgent (Harness)
     - 内置 bash/read/write 的 coding agent
   * - Workspace
     - 限定 agent 只能操作临时目录
   * - Session
     - 保持多轮对话记忆
   * - Context Engine
     - 自动裁剪过长上下文
   * - Task Loop
     - 实时打印执行事件
   * - InputGuard (Security)
     - 独立的安全检查工具
