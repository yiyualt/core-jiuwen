## Context

提示词优化 = 搜索最佳 system_prompt。使用 LLM 分析失败案例生成改进。

## Decisions

**1. Case**

```python
@dataclass
class Case:
    input: dict     # {"query": "What's 2+2?"}
    expected: str   # "4"
```

**2. Evaluator**

```python
class Evaluator:
    def __init__(self, cases: list[Case]):
        self._cases = cases

    async def evaluate(self, agent) -> dict:
        results = []
        for case in self._cases:
            result = await agent.run(case.input)
            actual = result.get("result", "")
            passed = case.expected.lower() in actual.lower()
            results.append({"case": case, "passed": passed, "actual": actual})
        score = sum(1 for r in results if r["passed"]) / len(results)
        return {"score": score, "results": results}
```

**3. Optimizer**

```python
class Optimizer:
    def __init__(self, client):
        self._client = client

    async def optimize(self, current_prompt, failures) -> str:
        # LLM analyzes failures and suggests improved prompt
        messages = [
            {"role": "system", "content": "You improve AI agent prompts."},
            {"role": "user", "content": f"Current prompt: {current_prompt}\nFailures: {failures}\nSuggest better prompt:"},
        ]
        response = await self._client.chat(messages)
        return response.strip()
```

**4. Trainer**

```python
class Trainer:
    def __init__(self, evaluator, optimizer, max_rounds=5):
        ...

    async def train(self, agent) -> dict:
        best_prompt = agent._system_prompt
        best_score = 0
        for round in range(self._max_rounds):
            result = await self._evaluator.evaluate(agent)
            if result["score"] > best_score:
                best_score = result["score"]
                best_prompt = agent._system_prompt
            if result["score"] == 1.0:
                break
            failures = [r for r in result["results"] if not r["passed"]]
            new_prompt = await self._optimizer.optimize(best_prompt, failures)
            agent._system_prompt = new_prompt
        return {"best_prompt": best_prompt, "best_score": best_score}
```

**5. 用 FakeLLMClient 测试**

Trainer 的 optimizer 使用 FakeLLMClient，Evaluator 直接调用 agent.run()。完全不依赖真实 LLM。
