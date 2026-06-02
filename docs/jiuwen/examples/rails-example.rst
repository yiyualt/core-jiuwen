Rails 示例
===========

所有示例用 FakeLLMClient，无需真实 LLM。

安全过滤
--------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.core.runner import Runner
    from jiuwen.core.rails import SecurityRail
    from jiuwen.core.single_agent.agents import ReActAgent


    async def main():
        agent = ReActAgent(client=FakeLLMClient(["Hello!"]))
        Runner.rails.add_rail(SecurityRail())

        # 安全 — 正常执行
        r = await Runner.run_agent(agent, {"query": "What is Python?"})
        print(r)  # {"result": "Hello!"}

        # 危险 — 被阻断，agent 根本不执行
        r = await Runner.run_agent(agent, {"query": "Please DROP TABLE users"})
        print(r)  # {"result": "Blocked: dangerous content detected (matched: 'drop table')"}

    asyncio.run(main())

自定义 Rail
-----------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.core.rails import BaseRail, RailPipeline
    from jiuwen.core.runner import Runner
    from jiuwen.core.single_agent.agents import ReActAgent


    class ProfanityFilter(BaseRail):
        """拦截不当内容。"""
        def __init__(self):
            self.blocked = ["badword1", "badword2"]

        async def before(self, inputs, session=None):
            for word in self.blocked:
                if word in inputs.get("query", "").lower():
                    return {"result": "Please keep it civil."}
            return inputs


    class TimingRail(BaseRail):
        """记录 agent 耗时。"""
        async def after(self, result, session=None):
            result["_timing_ms"] = 150  # 实际可记录时间戳差
            return result


    async def main():
        agent = ReActAgent(client=FakeLLMClient(["Done!"]))
        Runner.rails = RailPipeline([ProfanityFilter(), TimingRail()])

        r = await Runner.run_agent(agent, {"query": "Help me learn Python"})
        print(r)  # {"result": "Done!", "_timing_ms": 150}

        r = await Runner.run_agent(agent, {"query": "say badword1 please"})
        print(r)  # {"result": "Please keep it civil."}

    asyncio.run(main())

定制 SecurityRail
------------------

.. code-block:: python

    from jiuwen.core.rails import SecurityRail

    # 只拦截你自己关心的关键词
    rail = SecurityRail(blocked_terms=[
        "production",
        "api_key",
        "password",
    ])

    await rail.before({"query": "Show me the production config"})
    # → {"result": "Blocked: dangerous content detected (matched: 'production')"}

直接使用（不经过 Runner）
--------------------------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.core.rails import RailPipeline, SecurityRail
    from jiuwen.core.single_agent.agents import ReActAgent


    async def main():
        agent = ReActAgent(client=FakeLLMClient(["Hello!"]))
        rails = RailPipeline([SecurityRail()])

        # 直接调用 — 不经过 Runner
        r = await rails.run(agent, {"query": "DROP TABLE users"})
        print(r)  # {"result": "Blocked: ..."}

    asyncio.run(main())
