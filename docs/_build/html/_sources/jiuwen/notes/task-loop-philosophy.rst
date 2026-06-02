Task Loop: 事件驱动的 Agent 执行
====================================

**一句话：让 agent 的执行过程从黑盒变成可观察的。**

问题：agent.run() 是黑盒
--------------------------

直接调用 ``agent.run()``，你只能等结果 — 不知道中间发生了什么：

.. code-block:: python

    # 这样调用，你只能干等
    result = await agent.run({"query": "fix the bug"})
    # ... 10 秒后 ...
    print(result)  # 终于出结果了

    # 但你不知道：
    # - agent 调用了哪些工具？
    # - 哪一步慢了？
    # - 有没有出错？

解决：用事件流
----------------

Task Loop 在 agent 执行过程中不断发出事件，你可以监听：

.. code-block:: python

    from jiuwen.harness.task_loop import TaskExecutor, LoggingHandler

    executor = TaskExecutor(agent, handlers=[LoggingHandler()])
    result = await executor.execute("fix the bug")

    # 实时输出（不需要等 10 秒）：
    # [task_start] {'task': 'fix the bug'}
    # ... agent 执行中 ...
    # [task_complete] {'result': 'fixed!'}

就好比：直接调用是关灯洗照片，Task Loop 是开着灯看每一步。

三个实际场景
---------------

**场景 1：看 agent 在干什么**

.. code-block:: python

    executor = TaskExecutor(agent, handlers=[LoggingHandler()])
    result = await executor.execute("fix the bug")
    # stderr 实时输出事件

**场景 2：记录日志到文件**

.. code-block:: python

    class FileLogger(EventHandler):
        def __init__(self, path):
            self.f = open(path, "a")

        async def on_event(self, event):
            self.f.write(f"[{event.type}] {event.data}\n")

    executor = TaskExecutor(agent, handlers=[FileLogger("agent.log")])
    result = await executor.execute("task")
    # 所有事件写入 agent.log

**场景 3：批量处理任务**

.. code-block:: python

    coordinator = LoopCoordinator(executor)
    await coordinator.submit("Fix bug #42")
    await coordinator.submit("Add unit tests")
    await coordinator.submit("Update docs")
    await coordinator.submit(None)  # 停止
    await coordinator.run()
    # 三个任务顺序执行，每个都发出事件

对比总结
---------

.. list-table::
   :header-rows: 1

   * -
     - agent.run()
     - TaskExecutor
     - LoopCoordinator
   * - 观察性
     - 黑盒
     - 实时事件流
     - 事件 + 队列
   * - 日志
     - 没有
     - 任意 handler
     - 任意 handler
   * - 批量
     - 手动循环
     - 手动循环
     - 自动队列
   * - 监控
     - 做不到
     - 可加 metrics
     - 可加 metrics

核心组件
---------

.. code-block:: text

    TaskEvent            ← 一件事发生了（task_start / task_complete / error）
    EventHandler         ← 对事件做出反应（写日志、发通知、记指标）
    TaskExecutor         ← 包装 agent.run()，执行时发出事件
    LoopCoordinator      ← 管理任务队列，按顺序执行
