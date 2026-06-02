Auto Harness 教程 — 自动优化框架
===================================

用 DeepAgent 自动优化 agent 的提示词和配置。标准化管道：评估 → 计划 → 实施 → 验证。

1. Pipeline — 管道
-------------------

预定义的标准四阶段优化管道。

.. code-block:: python

    from jiuwen.auto_harness import PipelineSpec, StageSpec, default_pipeline

    pipe = default_pipeline()
    # assess → plan → implement → verify

    for stage in pipe.stages:
        print(f"{stage.name}: {stage.description}")

    # 自定义管道
    my_pipe = PipelineSpec(name="custom", stages=[
        StageSpec("analyze", "Analyze code quality", "You are a code reviewer."),
        StageSpec("fix", "Fix identified issues", "You are a senior developer."),
    ])

2. Orchestrator — 编排
-----------------------

运行管道，每个 stage 使用专门的 agent。

.. code-block:: python

    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.auto_harness import AutoHarnessOrchestrator

    client = OpenAIClient.from_env()
    orchestrator = AutoHarnessOrchestrator(client)

    result = await orchestrator.run("Optimize the database query performance")

    for stage_name, stage_result in result["results"].items():
        print(f"{stage_name}: {stage_result['result'][:100]}...")

3. Experience — 经验
---------------------

积累优化经验，跨运行学习。

.. code-block:: python

    from jiuwen.auto_harness import ExperienceStore

    store = ExperienceStore()

    # 记录每次运行
    store.record("assess", "fix bug #42", {"result": "Found 3 issues"})
    store.record("implement", "fix bug #42", {"result": "All 3 fixed"})

    # 查询历史
    recent = store.recent(stage="assess", limit=5)
    all_records = store.recent()  # 全部

    print(f"Total experiences: {len(store)}")
    store.clear()
