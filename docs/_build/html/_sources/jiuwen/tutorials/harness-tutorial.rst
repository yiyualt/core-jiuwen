Harness 教程 — Coding Agent 框架
=====================================

Harness 在 core SDK 之上构建了完整的 coding agent。内置编码工具，开箱即用。

1. DeepAgent — 核心
--------------------

内置 bash / read / write 三个编码工具，继承 ReActAgent。

.. code-block:: python

    from jiuwen.harness import DeepAgent, DeepAgentConfig, create_deep_agent
    from jiuwen.core.foundation import OpenAIClient

    # 零配置
    agent = create_deep_agent(workspace_dir="./my-project")

    # 完整配置
    client = OpenAIClient.from_env()
    agent = DeepAgent(client, DeepAgentConfig(
        workspace_dir="./my-project",
        system_prompt="You are a Python expert.",
        max_iterations=30,
    ))

    result = await agent.run({"query": "Create hello.py that prints 'Hello, World!'"})

2. Workspace — 工作区
-----------------------

限定 agent 只能操作指定目录。路径逃逸自动拦截。

.. code-block:: python

    from jiuwen.harness import Workspace

    ws = Workspace("/project")
    ws.write_file("src/main.py", "print('hello')")
    ws.write_file("../etc/passwd", "evil")  # → ValueError!

    files = ws.list_files("**/*.py")        # glob 模式
    content = ws.read_file("src/main.py")

3. Prompt Builder — 提示词
----------------------------

分层构建 system prompt。

.. code-block:: python

    from jiuwen.harness.prompts import (
        PromptBuilder, IdentitySection, ToolsSection, SafetySection,
    )

    builder = PromptBuilder([
        IdentitySection(role="Python expert"),
        ToolsSection(),
        SafetySection(),
    ])
    prompt = builder.build({"workspace": "/project"})

4. Task Loop — 事件循环
------------------------

可观察的 agent 执行。实时看到每一步。

.. code-block:: python

    from jiuwen.harness.task_loop import TaskExecutor, LoggingHandler, LoopCoordinator

    # 单任务
    executor = TaskExecutor(agent, handlers=[LoggingHandler()])
    result = await executor.execute("fix the bug")

    # 批量
    coordinator = LoopCoordinator(executor)
    await coordinator.submit("Fix bug #1")
    await coordinator.submit("Fix bug #2")
    await coordinator.submit(None)  # 停止信号
    await coordinator.run()
