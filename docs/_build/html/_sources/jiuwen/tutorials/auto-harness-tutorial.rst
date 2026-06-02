Auto Harness 教程 — 自动优化框架
===================================

用专门的 agent 管道自动优化代码。每个阶段由不同角色（审查员→架构师→开发者→测试员）的 agent 执行。

.. note::

   以下代码均可直接运行。使用 FakeLLMClient 不需要真实 API。

1. Orchestrator — 一行运行
---------------------------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.auto_harness import AutoHarnessOrchestrator


    async def main():
        client = FakeLLMClient([
            "Final Answer: 发现 3 个问题：性能瓶颈、缺少日志、异常未处理",
            "Final Answer: 方案：1.优化查询 2.添加日志 3.捕获异常",
            "Final Answer: 已修改 main.py 和 db.py，实现了上述方案",
            "Final Answer: 所有测试通过，性能提升 30%",
        ])

        orch = AutoHarnessOrchestrator(client)
        result = await orch.run("优化数据库查询性能")

        for stage_name, data in result["results"].items():
            print(f"[{stage_name}] {data['output'][:80]}...")

        print(f"管道: {result['pipeline']}，共 {len(result['results'])} 个阶段")

    asyncio.run(main())

输出::

    [assess] 发现 3 个问题：性能瓶颈、缺少日志、异常未处理...
    [plan] 方案：1.优化查询 2.添加日志 3.捕获异常...
    [implement] 已修改 main.py 和 db.py...
    [verify] 所有测试通过，性能提升 30%...
    管道: standard，共 4 个阶段

2. 选择管道
-----------

两种内置管道: ``standard`` (4 阶段) 和 ``extended`` (5 阶段, 多一轮评估)。

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.auto_harness import AutoHarnessOrchestrator


    async def main():
        client = FakeLLMClient([
            "Final Answer: 第一轮评估", "Final Answer: 第二轮评估",
            "Final Answer: 计划", "Final Answer: 实施", "Final Answer: 验证",
        ])

        orch = AutoHarnessOrchestrator(client)

        # 使用 extended 管道
        result = await orch.run("重构代码", pipeline_name="extended")
        print(f"管道: {result['pipeline']}，阶段数: {len(result['results'])}")
        # 管道: extended，阶段数: 5

    asyncio.run(main())

3. 流式执行 — 实时看到每个阶段的结果
-------------------------------------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.auto_harness import AutoHarnessOrchestrator


    async def main():
        client = FakeLLMClient([
            "Final Answer: 评估结果", "Final Answer: 计划方案",
            "Final Answer: 实施完成", "Final Answer: 验证通过",
        ])

        orch = AutoHarnessOrchestrator(client)

        # 流式 — 每完成一个阶段就立即输出
        async for stage_result in orch.run_stream("优化代码"):
            print(f"✓ {stage_result.stage_name} 完成: {stage_result.output[:60]}...")

    asyncio.run(main())

输出::

    ✓ assess 完成: 评估结果...
    ✓ plan 完成: 计划方案...
    ✓ implement 完成: 实施完成...
    ✓ verify 完成: 验证通过...

4. Experience — 跨运行学习
---------------------------

.. code-block:: python

    from jiuwen.auto_harness import ExperienceStore

    store = ExperienceStore()

    store.record("assess", "任务1", {"result": "发现 3 个问题"})
    store.record("implement", "任务1", {"result": "已全部修复"})

    recent = store.recent(stage="assess", limit=5)
    print(f"最近评估记录: {len(recent)} 条")
    print(f"总经验: {len(store)} 条")

    store.clear()
