Rails: Agent 中间件系统
=========================

Rails 是 **可组合的 before/after 钩子**，在 agent 执行前后拦截请求和响应。
类似于 Web 框架的 middleware（Express.js / Django middleware），但针对 AI agent。

架构位置
--------

Rails 位于 **core 层** (通用 SDK)，harness 和所有 agent 都可以用它：

.. code-block:: text

    jiuwen/
    ├── core/rails/          ← 通用中间件框架
    │   ├── BaseRail          (before/after 钩子)
    │   ├── RailPipeline      (编排多个 rail)
    │   └── SecurityRail      (拦截危险输入)
    │
    ├── core/runner/          ← Runner 持有 RailPipeline
    │   └── Runner.rails       (对 Runner.run_agent 的所有调用都经过 rails)
    │
    └── harness/              ← coding agent 也用 rails
        └── DeepAgent          (通过 Runner 自动受保护)

执行顺序
--------

.. code-block:: text

    用户调用 Runner.run_agent(agent, inputs)
    │
    ├─→ Rail A.before(inputs)   ← 可以修改/拦截输入
    │   └─→ Rail B.before(inputs)
    │       └─→ agent.run(inputs)   ← 核心执行
    │           └─→ Rail B.after(result)  ← 逆序
    │               └─→ Rail A.after(result)
    │
    └─→ 返回最终结果

关键：after 钩子是**逆序**执行的（洋葱模型）。

三种能力
--------

.. list-table::
   :header-rows: 1

   * - 能力
     - 说明
     - 示例
   * - **检查**
     - 读取输入/输出，不做修改
     - 日志记录、审计追踪
   * - **修改**
     - 改变数据再传递
     - 脱敏、追加上下文
   * - **阻断**
     - 直接返回结果，不调用 agent
     - 安全检查、内容过滤

阻断（Short-Circuit）机制
-------------------------

如果 before() 返回 ``{"result": "..."}``，pipeline 会**跳过 agent** 直接返回：

.. code-block:: python

    class SecurityRail(BaseRail):
        async def before(self, inputs, session=None):
            query = inputs.get("query", "").lower()
            for term in ["drop table", "rm -rf"]:
                if term in query:
                    # 返回带 "result" 键的 dict = 阻断
                    return {"result": f"Blocked: dangerous content"}
            # 返回原始 inputs = 放行
            return inputs

    # 使用：
    rail = SecurityRail()
    result = await rail.before({"query": "Please DROP TABLE users"})
    # → {"result": "Blocked: dangerous content"}    ← agent 不会被调用

    result = await rail.before({"query": "What is Python?"})
    # → {"query": "What is Python?"}                ← 正常放行

自定义 Rail 示例
-----------------

**日志 Rail：**

.. code-block:: python

    class LoggingRail(BaseRail):
        async def before(self, inputs, session=None):
            print(f"[进入] {inputs.get('query', '')[:100]}")
            return inputs

        async def after(self, result, session=None):
            print(f"[返回] {str(result.get('result', ''))[:100]}")
            return result

**内容过滤 Rail：**

.. code-block:: python

    class ContentFilterRail(BaseRail):
        def __init__(self, blocked_words):
            self._blocked = blocked_words

        async def before(self, inputs, session=None):
            text = inputs.get("query", "").lower()
            for word in self._blocked:
                if word in text:
                    return {"result": "请文明交流。"}
            return inputs

**文件保护 Rail：**

.. code-block:: python

    class ReadOnlyRail(BaseRail):
        """禁止 agent 写入任何文件（只读模式）。"""
        async def before(self, inputs, session=None):
            inputs["_readonly"] = True
            return inputs

        async def after(self, result, session=None):
            # 审计：记录 agent 做了什么
            return result

集成到 Runner
--------------

Runner 持有全局 RailPipeline，所有 agent 调用自动经过 rails：

.. code-block:: python

    from jiuwen.core.runner import Runner
    from jiuwen.core.rails import SecurityRail

    # 全局生效 — 所有 agent 都受保护
    Runner.rails.add_rail(SecurityRail())

    # DeepAgent（harness）、ReActAgent、WorkflowAgent 都经过这里
    result = await Runner.run_agent(any_agent, {"query": "..."})

Pipeline 可以组合多个 rail：

.. code-block:: python

    from jiuwen.core.rails import RailPipeline, SecurityRail

    Runner.rails = RailPipeline([
        SecurityRail(),       # 先检查安全
        LoggingRail(),        # 再记录日志
        ContentFilterRail(),  # 最后过滤内容
    ])
    # 执行顺序：Security.before → Logging.before → Content.before → agent
    #                                                        → Content.after
    #                                                   → Logging.after
    #                                              → Security.after
