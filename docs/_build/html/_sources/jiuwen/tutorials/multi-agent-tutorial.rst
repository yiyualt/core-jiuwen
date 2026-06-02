Multi-Agent 教程 — 动态多 Agent 运行时
========================================

agent_teams 是静态的（预定义成员），multi_agent 是动态的（运行时注册、发现、路由）。

1. MessageBus — 消息总线
--------------------------

发布订阅模式，多对多通信。

.. code-block:: python

    from jiuwen.core.multi_agent import MessageBus

    bus = MessageBus()

    async def log_handler(msg):
        print(f"[LOG] {msg}")

    bus.subscribe("tasks", log_handler)
    await bus.publish("tasks", {"task": "search", "query": "AI"})

    # 多个 handler 并发执行
    bus.subscribe("tasks", another_handler)
    await bus.publish("tasks", {"task": "analyze"})

2. TeamRuntime — 运行时
-------------------------

按能力标签路由任务到最合适的 agent。

.. code-block:: python

    from jiuwen.core.multi_agent import TeamRuntime

    rt = TeamRuntime()

    rt.register("coder", coder_agent, capabilities=["python", "debug", "test"])
    rt.register("writer", writer_agent, capabilities=["docs", "blog"])
    rt.register("analyst", analyst_agent, capabilities=["data", "sql", "stats"])

    # 自动路由
    best = rt.route("fix python bug in main.py")  # → "coder"
    best = rt.route("write a blog post about AI")  # → "writer"
    best = rt.route("analyze sales data")          # → "analyst"

    # 注销
    rt.unregister("coder")

    # 广播
    await rt.broadcast("announcements", {"msg": "new task available"})

3. Handoff — 任务交接
----------------------

一个 agent 把任务转交给另一个。

.. code-block:: python

    from jiuwen.core.multi_agent import handoff
    from jiuwen.core.session import Session

    session = Session()

    # Coder 做不到，转给 Writer
    result = await handoff(
        source_agent=coder_agent,
        target_agent=writer_agent,
        task="Write documentation for the new API",
        session=session,
    )


.. note::

   multi_agent 适合**动态 agent 池**的发现和路由。如果需要**预定义团队和 LLM 委派**，请看 :doc:`/jiuwen/tutorials/agent-teams-tutorial`。

   两者的详细对比见 :doc:`/jiuwen/notes/teams-philosophy`。
