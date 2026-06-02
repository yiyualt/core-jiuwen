Getting Started
================

安装
----

.. code-block:: bash

    pip install -e .
    # 或
    uv sync

配置 LLM（可选，测试不需要）：

.. code-block:: bash

    cp .env.example .env
    # 编辑 .env 填入你的 API key

.. code-block:: text

    OPENAI_API_KEY=sk-your-key
    OPENAI_API_BASE=https://api.openai.com/v1
    OPENAI_MODEL=gpt-4o

第一个例子
----------

.. code-block:: python

    import asyncio
    from jiuwen.core.foundation import OpenAIClient
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig

    async def main():
        client = OpenAIClient.from_env()
        config = LLMCompConfig(template_content=[
            {"role": "user", "content": "{{query}}"},
        ])

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("llm", LLMComponent(config, client))
        wf.set_end_comp("end", End({"responseTemplate": "{{output}}"}))

        wf.add_connection("start", "llm")
        wf.add_connection("llm", "end")

        result = await wf.invoke({"query": "Hello, who are you?"})
        print(result.result)

    asyncio.run(main())

继续学习
--------

按主题深入：

- :doc:`/jiuwen/tutorials/core-tutorial` — Core SDK 核心原语
- :doc:`/jiuwen/tutorials/harness-tutorial` — Harness Coding Agent 框架
- :doc:`/jiuwen/tutorials/agent-teams-tutorial` — 多 Agent 协作
- :doc:`/jiuwen/tutorials/multi-agent-tutorial` — 动态多 Agent 运行时
- :doc:`/jiuwen/tutorials/auto-harness-tutorial` — 自动优化框架
