Agent Teams: Multi-Agent Collaboration
=========================================

A **Team** bundles specialized agents under a **Coordinator** that
breaks complex tasks into subtasks and delegates each to the right expert.

Architecture
------------

.. code-block:: text

    User: "Research AI safety and write a report"

    Team
    ├── Coordinator (ReActAgent with delegate tool)
    │   ├── Thought: Need research
    │   ├── Action: delegate("researcher", "AI safety")
    │   ├── Observation: "AI safety concerns: ..."
    │   ├── Thought: Now write
    │   ├── Action: delegate("writer", "Write report about...")
    │   └── Final Answer: the report
    │
    └── Members
        ├── Researcher (ReActAgent with search tools)
        └── Writer (ReActAgent, no tools)

Usage
-----

.. code-block:: python

    from jiuwen.core.single_agent.agents import ReActAgent
    from jiuwen.core.agent_teams import Team
    from jiuwen.core.foundation import OpenAIClient, ToolCard

    client = OpenAIClient.from_env()

    # Create specialists
    researcher = ReActAgent(
        client, tools=[search_tool],
        system_prompt="You are a research specialist. Find facts.",
    )
    writer = ReActAgent(
        client,
        system_prompt="You are a technical writer. Write clearly.",
    )

    # Form a team
    team = Team(members={"researcher": researcher, "writer": writer})
    result = await team.run("Research renewable energy and write a summary")
    print(result["result"])

How It Works
------------

Coordinator inherits from ReActAgent with a built-in ``delegate`` tool.
It automatically:
1. Analyzes the task
2. Picks the right member for each subtask
3. Collects results
4. Synthesizes a final answer

agent_teams vs multi_agent
----------------------------

jiuwen 有两个多 agent 模块，职责不同：

.. list-table::
   :header-rows: 1

   * -
     - **agent_teams** (静态团队)
     - **multi_agent** (动态运行时)
   * - 成员
     - 创建时固定，不可变
     - 运行时动态注册/注销
   * - 任务分配
     - Coordinator LLM 推理委派
     - 关键词匹配自动路由
   * - 通信
     - InProcessMessager 点对点
     - MessageBus 发布订阅
   * - 任务状态
     - TaskBlueprint 跟踪生命周期
     - handoff 任务交接
   * - 适用场景
     - 已知团队分工（如：研究员+作家）
     - 动态 agent 池（如：插件市场）

.. code-block:: python

    # agent_teams: 成员固定，LLM 分配
    team = Team(members={"coder": coder, "writer": writer})
    result = await team.run("write a function and document it")
    # Coordinator 用 delegate("coder", ...) 和 delegate("writer", ...)

    # multi_agent: 动态注册，关键词路由
    rt = TeamRuntime()
    rt.register("coder", agent, capabilities=["python", "debug"])
    rt.register("analyst", agent, capabilities=["sql", "stats"])
    best = rt.route("fix python bug")   # → "coder"
    rt.unregister("coder")              # 随时移除

两者互补：用 multi_agent 做注册发现，用 agent_teams 做已知团队的协作委派。
