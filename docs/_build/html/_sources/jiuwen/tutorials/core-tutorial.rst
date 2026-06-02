Core SDK 教程
==============

jiuwen core 提供构建 AI agent 的底层原语。每个模块独立可用，也可以组合。

1. 身份 — BaseCard
------------------

所有组件的身份名片。每个 agent、tool、workflow 都继承它。

.. code-block:: python

    from jiuwen.core.common import BaseCard

    card = BaseCard(name="my_agent", description="My first agent")
    print(card.id, card.name, card.to_str())

    # 子类化
    class AgentCard(BaseCard):
        version: str = "0.1.0"
        model: str = "gpt-4o"

2. 图引擎 — Graph
------------------

``PregelGraph`` 构建 DAG，``Executable`` 是可执行节点。Workflow 底层就是图。

.. code-block:: python

    from jiuwen.core.graph import PregelGraph, Executable

    class EchoNode(Executable):
        async def on_invoke(self, inputs, **kwargs):
            return {"output": inputs["value"]}

    g = PregelGraph()
    g.add_node("echo", EchoNode())
    g.start_node("echo").end_node("echo")
    compiled = g.compile()
    result = await compiled._invoke({"value": "hello"})

3. 工作流 — Workflow
--------------------

``Workflow`` 封装组件管道。Start → Components → End。

.. code-block:: python

    from jiuwen.core.workflow import Workflow, Start, End

    wf = Workflow()
    wf.set_start_comp("s", Start())
    wf.set_end_comp("e", End())
    wf.add_connection("s", "e")
    result = await wf.invoke({"msg": "hello"})

4. LLM — Foundation + Component
--------------------------------

``OpenAIClient`` 调用真实大模型。``LLMComponent`` 把 LLM 变成工作流节点。

.. code-block:: python

    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

    client = OpenAIClient.from_env()

    response = await client.chat([{"role": "user", "content": "Hello!"}])

    comp = LLMComponent(LLMCompConfig(
        template_content=[{"role": "user", "content": "{{query}}"}],
    ), client)
    result = await comp.invoke({"query": "What is AI?"})

5. 工具 — Tool
---------------

``ToolCard`` + ``ToolComponent`` 把 Python 函数变成工作流节点。

.. code-block:: python

    from jiuwen.core.foundation import ToolCard, ToolComponent

    def add(a: int, b: int) -> int:
        return a + b

    card = ToolCard(name="add", func=add)
    result = await ToolComponent(card).invoke({"a": 3, "b": 4})  # → {"output": 7}

    # 也支持 async 函数
    async def fetch(url: str) -> str:
        return f"data from {url}"
    result = await ToolComponent(ToolCard(name="fetch", func=fetch)).invoke({"url": "..."})

6. Agent — ReActAgent
-----------------------

自主推理 + 选工具 + 执行。循环 Thought → Action → Observation。

.. code-block:: python

    from jiuwen.core.single_agent.agents import ReActAgent

    agent = ReActAgent(client=client, tools=[search_tool, calc_tool])
    result = await agent.run({"query": "What is 15 * 7 plus 3?"})

7. 执行入口 — Runner
---------------------

``Runner`` 统一入口 + 全局资源注册。所有 agent 通过 Runner 执行。

.. code-block:: python

    from jiuwen.core.runner import Runner

    Runner.resource_mgr.add_workflow("my_wf_1.0", lambda: create_my_wf())
    result = await Runner.run_agent(agent, {"query": "hello"})

8. 会话 — Session
------------------

``Session`` 多轮记忆。agent 记住之前的对话。

.. code-block:: python

    from jiuwen.core.session import Session

    session = Session()
    await agent.run({"query": "I'm Bob"}, session=session)
    await agent.run({"query": "What's my name?"}, session=session)  # 记得名字!

9. 条件 — Branch
-----------------

``ExpressionCondition`` + ``BranchComponent`` 实现 if/else 路由。

.. code-block:: python

    from jiuwen.core.workflow.components import ExpressionCondition, BranchComponent

    branch = BranchComponent(ExpressionCondition("{{score}} >= 60"))

    def router(state):
        return "pass" if state.get("branch_result") else "fail"

    wf.add_conditional_connection("check", router)

10. 中间件 — Rails
-------------------

Rails 拦截 agent 输入输出。安全、日志、审计都可以用。

.. code-block:: python

    from jiuwen.core.rails import SecurityRail, RailPipeline
    from jiuwen.core.runner import Runner

    Runner.rails = RailPipeline([SecurityRail()])
    # 所有 agent 调用自动检查危险输入

11. 上下文 — Context Engine
----------------------------

管理 LLM 上下文窗口。token 计数 + 自动裁剪旧消息。

.. code-block:: python

    from jiuwen.core.context_engine import ModelContext

    ctx = ModelContext(max_tokens=4096)
    ctx.add_system("You are helpful.")
    ctx.add_user("Hello!")
    msgs = ctx.get_messages()  # 自动裁剪到 4096 tokens

12. 安全 — Security
--------------------

独立的输入/输出/路径安全检查。

.. code-block:: python

    from jiuwen.core.security import InputGuard, OutputGuard, PathSecurity

    InputGuard.check("rm -rf /")             # → False
    OutputGuard.check("API key: sk-abc...")   # → False
    PathSecurity.is_safe("/proj", "../etc")   # → False

13. 系统操作 — Sys Operation
------------------------------

安全执行代码、Shell 命令、文件操作。

.. code-block:: python

    from jiuwen.core.sys_operation import CodeOperator, ShellOperator, FileOperator

    result = await CodeOperator(timeout=5).execute("print(1+1)")
    result = await ShellOperator(allowed_commands=["ls"]).execute("ls")
    result = FileOperator("/tmp").write("test.txt", "hello")

14. 优化 — Agent Evolving
---------------------------

自动优化 agent 提示词。

.. code-block:: python

    from jiuwen.core.agent_evolving import Case, Evaluator, Optimizer, Trainer

    cases = [Case(input={"query": "2+2"}, expected="4")]
    trainer = Trainer(Evaluator(cases), Optimizer(client))
    result = await trainer.train(agent)
    agent._system_prompt = result["best_prompt"]

15. 扩展组件
-------------

额外的 Workflow 组件：追问、意图识别、HTTP 请求、循环。

.. code-block:: python

    from jiuwen.core.workflow.components import (
        QuestionerComponent,         # 缺少信息时追问
        IntentDetectionComponent,    # 关键词匹配意图
        HTTPRequestComponent,        # HTTP 请求
        LoopComponent,               # 循环累积
    )
