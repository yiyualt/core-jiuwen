# coding: utf-8
"""BranchComponent — a workflow component that evaluates conditions for routing.

Used with conditional edges to create if/else branches in workflows.
"""

from jiuwen.core.workflow.components.component import WorkflowComponent
from jiuwen.core.workflow.components.condition.condition import Condition


class BranchComponent(WorkflowComponent):
    """Evaluates a condition and outputs the boolean result.

    The output is used by a Router function attached via
    add_conditional_connection to determine which downstream
    node receives the data next.

    Usage::

        cond = ExpressionCondition("{{score}} >= 60")
        branch = BranchComponent(cond)

        # In workflow:
        wf.add_workflow_comp("check", branch)
        wf.add_conditional_connection("check", lambda s: (
            "pass_node" if s.get("branch_result") else "fail_node"
        ))
    """

    def __init__(self, condition: Condition):
        """Initialize with a condition.

        Args:
            condition: A Condition instance to evaluate.
        """
        super().__init__()
        self._condition = condition

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        """Evaluate the condition and return the result.

        Args:
            inputs: Input values to evaluate the condition against.

        Returns:
            Dict with "branch_result" key (True/False).
        """
        result = self._condition.evaluate(inputs)
        return {"branch_result": result}
