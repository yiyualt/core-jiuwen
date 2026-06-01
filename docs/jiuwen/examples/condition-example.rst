Condition Examples
===================

If-Else Pipeline
-----------------

.. code-block:: python

    import asyncio
    from jiuwen.core.workflow import Workflow, Start, End
    from jiuwen.core.workflow.components import (
        BranchComponent, ExpressionCondition,
    )
    from jiuwen.core.workflow.components import LLMComponent, LLMCompConfig


    async def main():
        cond = ExpressionCondition("{{score}} >= 60")
        branch = BranchComponent(cond)

        # Two different LLM responses based on score
        pass_component = LLMComponent(LLMCompConfig(
            template_content=[{"role": "user", "content": "Say congratulations! Score: {{score}}"}],
        ))
        fail_component = LLMComponent(LLMCompConfig(
            template_content=[{"role": "user", "content": "Give encouragement. Score: {{score}}"}],
        ))

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("check", branch)
        wf.add_workflow_comp("pass_branch", pass_component)
        wf.add_workflow_comp("fail_branch", fail_component)
        wf.set_end_comp("end", End())

        wf.add_connection("start", "check")

        def router(state):
            return "pass_branch" if state.get("branch_result") else "fail_branch"

        wf.add_conditional_connection("check", router)
        wf.add_connection("pass_branch", "end")
        wf.add_connection("fail_branch", "end")

        # Score >= 60
        result = await wf.invoke({"score": 85})
        print(result.state)  # COMPLETED (went through pass_branch)

    asyncio.run(main())

String-Based Routing
--------------------

.. code-block:: python

    from jiuwen.core.workflow.components import ExpressionCondition

    # Route based on string content
    cond = ExpressionCondition("{{language}} == 'Chinese'")
    cond.evaluate({"language": "Chinese"})  # True
    cond.evaluate({"language": "English"})  # False
