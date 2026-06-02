Auto Harness 示例
==================

所有示例用 FakeLLMClient，可直接运行。

基础 4 阶段管道
----------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation.llm import LLMClient, ModelRequestConfig
    from typing import AsyncIterator

    # Inline FakeLLMClient so the example is self-contained
    class FakeLLMClient(LLMClient):
        def __init__(self, responses=None):
            self.responses = responses or ['default']
            self.call_count = 0
            self.last_messages = []
        async def chat(self, messages, config=None):
            self.last_messages = messages
            r = self.responses[self.call_count % len(self.responses)]
            self.call_count += 1
            return r
        async def chat_stream(self, messages, config=None):
            t = await self.chat(messages, config)
            yield t

    from jiuwen.auto_harness import AutoHarnessOrchestrator


    async def main():
        client = FakeLLMClient([
            "Final Answer: Found 3 issues: N+1 queries, missing indexes, no caching",
            "Final Answer: Plan: 1. Add eager loading 2. Create indexes 3. Add Redis cache",
            "Final Answer: Implemented all 3 changes in models.py and settings.py",
            "Final Answer: All tests pass. Query time reduced from 500ms to 50ms.",
        ])

        orch = AutoHarnessOrchestrator(client)
        result = await orch.run("Optimize database queries", pipeline_name="standard")

        for stage_name, data in result["results"].items():
            print(f"[{stage_name}] {data['output'][:80]}...")

        print(f"\\nPipeline: {result['pipeline']}, Experience entries: {len(orch.experience)}")

    asyncio.run(main())

输出::

    [assess] Found 3 issues: N+1 queries, missing indexes, no caching...
    [plan] Plan: 1. Add eager loading 2. Create indexes 3. Add Redis cache...
    [implement] Implemented all 3 changes in models.py and settings.py...
    [verify] All tests pass. Query time reduced from 500ms to 50ms....

    Pipeline: standard, Experience entries: 4

流式执行
--------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation.llm import LLMClient, ModelRequestConfig
    from typing import AsyncIterator

    class FakeLLMClient(LLMClient):
        def __init__(self, responses=None):
            self.responses = responses or ['default']
            self.call_count = 0
            self.last_messages = []
        async def chat(self, messages, config=None):
            self.last_messages = messages
            r = self.responses[self.call_count % len(self.responses)]
            self.call_count += 1
            return r
        async def chat_stream(self, messages, config=None):
            t = await self.chat(messages, config)
            yield t

    from jiuwen.auto_harness import AutoHarnessOrchestrator


    async def main():
        client = FakeLLMClient(["Final Answer: Done"] * 4)
        orch = AutoHarnessOrchestrator(client)

        # 每完成一个阶段立即输出
        async for stage in orch.run_stream("Add logging to auth module"):
            print(f"  [{stage.status}] {stage.stage_name}: {stage.output[:60]}...")

    asyncio.run(main())

Meta Evolve 会话级管道
-----------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation.llm import LLMClient
    from typing import AsyncIterator

    class FakeLLMClient(LLMClient):
        def __init__(self, responses=None):
            self.responses = responses or ['default']
            self.call_count = 0
            self.last_messages = []
        async def chat(self, messages, config=None):
            self.last_messages = messages
            r = self.responses[self.call_count % len(self.responses)]
            self.call_count += 1
            return r
        async def chat_stream(self, messages, config=None):
            t = await self.chat(messages, config)
            yield t

    from jiuwen.auto_harness import AutoHarnessOrchestrator


    async def main():
        # 7 stages: assess, plan, 2 tasks * 2 (implement+verify), learnings
        client = FakeLLMClient([
            "Final Answer: Assessment: code has error handling gaps and missing tests",
            "Final Answer: 1. Fix error handling 2. Add unit tests",
            "Final Answer: Implemented error handling with try/except in all functions",
            "Final Answer: Verified: all error paths now handled correctly",
            "Final Answer: Implemented 15 unit tests covering all functions",
            "Final Answer: Verified: 15/15 tests pass, coverage 85%",
            "Final Answer: Learnings: error handling improved, test coverage increased",
        ])

        orch = AutoHarnessOrchestrator(client)
        result = await orch.run("Improve code quality", pipeline_name="meta_evolve")

        print(f"Pipeline: {result['pipeline']}")
        print(f"Stages: {len(result['results'])}")
        for name, data in result["results"].items():
            print(f"  [{name}] {data['output'][:70]}...")

        # 经验已持久化 (如果提供了 file_path)
        print(f"\\nExperience entries: {len(orch.experience)}")

    asyncio.run(main())

持久化经验 + 搜索
------------------

.. code-block:: python

    from jiuwen.auto_harness import ExperienceStore

    store = ExperienceStore("my_experiences.jsonl")

    # 记录
    store.record("assess", "优化数据库", {"result": "发现 N+1 查询"}, exp_type=store.SUCCESS)
    store.record_failure("verify", "添加缓存", "测试超时")
    store.record_insight("learnings", "数据库优化", "大表加索引前先分析")

    # 搜索
    results = store.search("database N+1")
    for r in results:
        print(f"[{r['type']}] {r['task']}: {r['summary'][:100]}")

    # 合成上下文 (注入 agent prompt)
    context = store.synthesize(results, max_tokens=1000)
    print(context)

    # 清理
    import os; os.remove("my_experiences.jsonl") if os.path.exists("my_experiences.jsonl") else None

Fix Loop 单独使用
------------------

.. code-block:: python

    import asyncio
    from jiuwen.auto_harness import FixLoopController, FixLoopResult


    async def main():
        fix = FixLoopController(phase1_max_retries=3, phase2_max_retries=1)

        attempts = 0

        async def verify():
            nonlocal attempts
            attempts += 1
            if attempts >= 2:
                return FixLoopResult(success=True, attempts=attempts, output="CI passed!")
            return FixLoopResult(success=False, error_log=["test_login failed: assertion error"])

        async def fix_errors(errors):
            print(f"  Fixing: {errors}")

        result = await fix.run(verify, fix_errors)
        print(f"Success: {result.success}, Attempts: {result.attempts}, Phase: {result.phase}")

    asyncio.run(main())

输出::

      Fixing: ['test_login failed: assertion error']
    Success: True, Attempts: 2, Phase: 1
