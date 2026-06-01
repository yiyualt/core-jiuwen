Condition & Branch: Control Flow in Workflows
================================================

Conditions turn linear pipelines into dynamic control flows
with if/else branching.

How It Works
------------

.. code-block:: text

    Without Condition:           With Condition:

    Start → A → B → End           Start → check ─┬─→ pass → End
                                                   └─→ fail → End

ExpressionCondition
-------------------

``ExpressionCondition`` evaluates ``{{variable}}`` templates as
Python boolean expressions:

.. code-block:: python

    from jiuwen.core.workflow.components import ExpressionCondition

    cond = ExpressionCondition("{{score}} >= 60")
    cond.evaluate({"score": 85})   # True
    cond.evaluate({"score": 50})   # False

    cond = ExpressionCondition("{{status}} == 'active'")
    cond.evaluate({"status": "active"})  # True

BranchComponent
---------------

``BranchComponent`` wraps a Condition into a workflow node:

.. code-block:: python

    from jiuwen.core.workflow.components import BranchComponent, ExpressionCondition

    branch = BranchComponent(ExpressionCondition("{{age}} >= 18"))

    # In workflow: connect via conditional edge with router
    wf.add_workflow_comp("check", branch)

    def router(state):
        return "adult" if state.get("branch_result") else "minor"

    wf.add_conditional_connection("check", router)
    wf.add_connection("adult", end)     # True branch
    wf.add_connection("minor", end)     # False branch
