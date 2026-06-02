扩展组件示例
==============

意图路由 Pipeline
-------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import (
        IntentDetectionComponent, BranchComponent, LLMComponent, LLMCompConfig,
    )
    from tests.conftest import FakeLLMClient


    async def main():
        # 意图识别
        intents = {
            "天气": ["天气", "温度"],
            "股票": ["股票", "股价"],
        }
        intent_comp = IntentDetectionComponent(intents)

        # 两个专业的 LLM 组件
        weather_llm = LLMComponent(
            LLMCompConfig(template_content=[
                {"role": "user", "content": "你是天气助手，回答: {{query}}"}
            ]),
            FakeLLMClient(["今天晴天，25度"]),
        )
        stock_llm = LLMComponent(
            LLMCompConfig(template_content=[
                {"role": "user", "content": "你是股票助手，回答: {{query}}"}
            ]),
            FakeLLMClient(["当前股价 150 元"]),
        )

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("intent", intent_comp)
        wf.add_workflow_comp("weather", weather_llm)
        wf.add_workflow_comp("stock", stock_llm)
        wf.set_end_comp("end", End())

        wf.add_connection("start", "intent")

        def router(state):
            intent = state.get("intent", "")
            return "weather" if intent == "天气" else "stock"

        wf.add_conditional_connection("intent", router)
        wf.add_connection("weather", "end")
        wf.add_connection("stock", "end")

        result = await wf.invoke({"query": "今天天气怎么样"})
        print(result.state)  # COMPLETED

    asyncio.run(main())

Loop + LLM 批量处理
--------------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import LoopComponent, LLMComponent, LLMCompConfig
    from tests.conftest import FakeLLMClient


    async def main():
        loop = LoopComponent(max_iterations=3)

        # 先收集 3 条输入
        await loop.invoke({"item": "bug: 登录失败"})
        await loop.invoke({"item": "bug: 页面空白"})
        result = await loop.invoke({"item": "bug: 数据丢失"})
        # result["done"] == True

        # 把所有 bug 一起发给 LLM 分析
        llm = LLMComponent(
            LLMCompConfig(template_content=[
                {"role": "user", "content": "分析这些 bug: {{items}}"}
            ]),
            FakeLLMClient(["这些都是严重问题"]),
        )
        summary = await llm.invoke({"items": str(result["items"])})
        print(summary)

    asyncio.run(main())

HTTP 调用 API
--------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow.components import HTTPRequestComponent


    async def main():
        comp = HTTPRequestComponent(
            "https://jsonplaceholder.typicode.com/{{resource}}"
        )

        result = await comp.invoke({"resource": "posts/1"})
        print(result["status"])  # 200
        print(result["body"][:100])

    asyncio.run(main())
