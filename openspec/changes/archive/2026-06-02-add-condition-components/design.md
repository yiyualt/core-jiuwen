## Context

Workflow 需要分支和条件能力。最简单的实现：Condition 抽象 + BranchComponent。

## Decisions

**1. Condition ABC**

```python
class Condition(ABC):
    @abstractmethod
    def evaluate(self, state: dict) -> bool: ...
```

**2. ExpressionCondition — 模板表达式**

```python
class ExpressionCondition(Condition):
    def __init__(self, expression: str):  # e.g. "{{score}} > 60"
    def evaluate(self, state):  # 渲染模板 → eval
```

**3. BranchComponent — if/else 路由**

```python
class BranchComponent(WorkflowComponent):
    def __init__(self, condition: Condition):
        self._condition = condition

    async def invoke(self, inputs, **kwargs) -> dict:
        result = self._condition.evaluate(inputs)
        return {"branch_result": result}
```

结合 PregelGraph.add_conditional_edges(source, router)，BranchComponent 输出 `{branch_result: True/False}` 被 Router 函数消费来路由到对应下游。

**4. 用法**

```python
wf = Workflow()
wf.set_start_comp("start", Start())
wf.add_workflow_comp("check", BranchComponent(ExpressionCondition("{{score}} > 60")))
wf.add_workflow_comp("pass_msg", EchoNode("Pass!"))
wf.add_workflow_comp("fail_msg", EchoNode("Fail!"))

wf.add_connection("start", "check")

# Route based on branch_result
def branch_router(state: dict) -> str:
    return "pass_msg" if state.get("branch_result") else "fail_msg"

wf.add_conditional_connection("check", branch_router)
wf.add_connection("pass_msg", "end")
wf.add_connection("fail_msg", "end")
wf.set_end_comp("end", End())
```
