扩展组件：Questioner / Intent / HTTP / Loop
=============================================

v0.18.0 新增四个组件，补全 workflow 的常见需求。

QuestionerComponent — 缺少信息时追问
--------------------------------------

当 pipeline 需要用户提供某个字段才能继续时，用它来**中断**执行并要求补充：

.. code-block:: python

    comp = QuestionerComponent("请输入你的名字", "name")

    # 有值 → 通过
    result = await comp.invoke({"name": "Alice"})
    # {"output": "Alice"}

    # 无值 → 追问
    result = await comp.invoke({})
    # {"question": "请输入你的名字", "field": "name"}

典型用法：放在 workflow 开头，保证后续节点有完整数据。

IntentDetectionComponent — 意图识别
--------------------------------------

基于关键词匹配识别用户意图，用于**路由**：

.. code-block:: python

    intents = {
        "查询天气": ["天气", "温度", "下雨"],
        "查询股票": ["股票", "股价", "涨跌"],
        "闲聊":    ["你好", "谢谢", "再见"],
    }
    comp = IntentDetectionComponent(intents)

    result = await comp.invoke({"query": "今天天气怎么样"})
    # {"intent": "查询天气", "confidence": 1.0}

    result = await comp.invoke({"query": "帮我写代码"})
    # {"intent": "unknown", "confidence": 0.0}

配合 BranchComponent 可以实现按意图路由到不同的下游处理。

HTTPRequestComponent — 调用外部 API
--------------------------------------

用 ``{{变量}}`` 模板构造 URL，发起 HTTP 请求：

.. code-block:: python

    comp = HTTPRequestComponent("https://api.example.com/{{endpoint}}")

    result = await comp.invoke({
        "endpoint": "users",
        "body": {"name": "Alice"},
    })
    # {"status": 200, "body": "..."}

支持 GET / POST / PUT / DELETE，自动处理 URL 编码和 JSON body。

LoopComponent — 循环执行
--------------------------

重复执行，累积每次的结果：

.. code-block:: python

    comp = LoopComponent(max_iterations=3)

    await comp.invoke({"item": "第一章"})  # {"items": ["第一章"], "count": 1, "done": False}
    await comp.invoke({"item": "第二章"})  # {"items": ["第一章","第二章"], "count": 2, "done": False}
    await comp.invoke({"item": "第三章"})  # {"items": [...], "count": 3, "done": True}

    comp.reset()  # 重置，下一轮重新开始

可用于批量处理：收集 N 个输入后一次性交给 LLM 处理。
