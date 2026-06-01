# coding: utf-8
"""Tests for Condition and BranchComponent."""

import pytest
from jiuwen.core.workflow.components.condition import Condition, ExpressionCondition
from jiuwen.core.workflow.components.flow.branch_comp import BranchComponent


class TestExpressionCondition:
    def test_number_greater_than(self):
        cond = ExpressionCondition("{{x}} > 5")
        assert cond.evaluate({"x": 10}) is True
        assert cond.evaluate({"x": 3}) is False

    def test_number_equality(self):
        cond = ExpressionCondition("{{score}} == 100")
        assert cond.evaluate({"score": 100}) is True
        assert cond.evaluate({"score": 99}) is False

    def test_string_equality(self):
        cond = ExpressionCondition("{{name}} == 'Bob'")
        assert cond.evaluate({"name": "Bob"}) is True
        assert cond.evaluate({"name": "Alice"}) is False

    def test_bool_direct(self):
        cond = ExpressionCondition("{{flag}}")
        assert cond.evaluate({"flag": True}) is True
        assert cond.evaluate({"flag": False}) is False

    def test_missing_var_defaults_false(self):
        cond = ExpressionCondition("{{missing}} > 5")
        assert cond.evaluate({}) is False

    def test_invalid_expr_defaults_false(self):
        cond = ExpressionCondition("{{x}} / 0")
        assert cond.evaluate({"x": 1}) is False


class TestBranchComponent:
    @pytest.mark.asyncio
    async def test_true_branch(self):
        cond = ExpressionCondition("{{ready}}")
        comp = BranchComponent(cond)
        result = await comp.invoke({"ready": True})
        assert result == {"branch_result": True}

    @pytest.mark.asyncio
    async def test_false_branch(self):
        cond = ExpressionCondition("{{done}}")
        comp = BranchComponent(cond)
        result = await comp.invoke({"done": False})
        assert result == {"branch_result": False}


class TestBranchInWorkflow:
    @pytest.mark.asyncio
    async def test_if_else_routing(self):
        from jiuwen.core.workflow import Workflow, Start, End
        from jiuwen.core.graph.executable import Executable

        class AppendNode(Executable[dict, dict]):
            def __init__(self, tag: str):
                self.tag = tag

            async def on_invoke(self, inputs: dict, **kwargs) -> dict:
                val = inputs.get("value", "")
                return {"value": f"{val}-{self.tag}"}

        cond = ExpressionCondition("{{score}} >= 60")
        branch = BranchComponent(cond)

        wf = Workflow()
        wf.set_start_comp("start", Start())
        wf.add_workflow_comp("check", branch)
        wf.add_workflow_comp("pass_node", AppendNode("pass"))
        wf.add_workflow_comp("fail_node", AppendNode("fail"))
        wf.set_end_comp("end", End())

        wf.add_connection("start", "check")

        def router(state: dict) -> str:
            return "pass_node" if state.get("branch_result") else "fail_node"

        wf.add_conditional_connection("check", router)
        wf.add_connection("pass_node", "end")
        wf.add_connection("fail_node", "end")

        # Score >= 60 → should go through pass_node
        result = await wf.invoke({"score": 85, "value": "test"})
        assert result.state.value == "COMPLETED"
