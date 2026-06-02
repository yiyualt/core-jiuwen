Agent Teams 教程 — 多 Agent 协作
=====================================

多个专业 agent 组成团队，Coordinator 分解任务并委派给合适的成员。

1. Team — 团队
---------------

Coordinator 自动分解任务、委派、汇总结果。

.. code-block:: python

    from jiuwen.core.agent_teams import Team
    from jiuwen.core.single_agent.agents import ReActAgent

    researcher = ReActAgent(client, tools=[search_tool], system_prompt="你是研究员")
    writer = ReActAgent(client, system_prompt="你是写作助手")

    team = Team(members={"researcher": researcher, "writer": writer})
    result = await team.run("Research AI safety and write a report")

2. CoordinatorAgent — 协调者
-----------------------------

直接使用 Coordinator，内置 delegate 工具。

.. code-block:: python

    from jiuwen.core.agent_teams.team import CoordinatorAgent

    coordinator = CoordinatorAgent(
        client=client,
        members={"coder": coder_agent, "reviewer": reviewer_agent},
        system_prompt="You manage a dev team.",
    )
    result = await coordinator.run({"query": "Write a sort function and review it"})

3. InProcessMessager — 消息
----------------------------

Agent 间异步消息传递。

.. code-block:: python

    from jiuwen.core.agent_teams import InProcessMessager

    msgr = InProcessMessager()

    # Agent A 发送
    await msgr.send("agent_b", {"task": "search", "query": "AI"})

    # Agent B 接收
    msg = await msgr.receive("agent_b")
    msg = await msgr.receive("agent_b", timeout=5.0)  # 带超时

4. TaskBlueprint — 任务
------------------------

跟踪任务生命周期。

.. code-block:: python

    from jiuwen.core.agent_teams import TaskBlueprint

    task = TaskBlueprint(task_id="t1", description="fix bug in auth.py")
    task.assigned_to = "coder"
    task.mark_running()
    task.mark_done({"result": "fixed"})

    print(task.status, task.result)

5. AgentSpawner — 生成
-----------------------

动态创建和注册 agent。

.. code-block:: python

    from jiuwen.core.agent_teams import AgentSpawner

    msgr = InProcessMessager()
    spawner = AgentSpawner(messager=msgr)

    coder = spawner.spawn("coder", lambda: ReActAgent(client, tools=[...]))
    writer = spawner.spawn("writer", lambda: ReActAgent(client))

    # 共享 messager，agent 之间可以通信
    await msgr.send("coder", {"task": "review this PR"})


.. note::

   agent_teams 适合**已知团队**的协作。如果需要**动态注册和关键词路由**，请看 :doc:`/jiuwen/tutorials/multi-agent-tutorial`。

   两者的详细对比见 :doc:`/jiuwen/notes/teams-philosophy`。
