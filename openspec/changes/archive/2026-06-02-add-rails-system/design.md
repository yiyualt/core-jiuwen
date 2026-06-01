## Context

Rails = 可组合的 before/after 拦截器。管道模式：before → agent.run → after。

## Decisions

**1. BaseRail**

```python
class BaseRail(ABC):
    async def before(self, inputs: dict, session=None) -> dict:
        return inputs  # default: pass through

    async def after(self, result: dict, session=None) -> dict:
        return result  # default: pass through
```

**2. RailPipeline**

```python
class RailPipeline:
    def __init__(self, rails=None):
        self._rails = rails or []

    async def run(self, agent, inputs, session=None):
        for rail in self._rails:
            inputs = await rail.before(inputs, session)
        result = await agent.run(inputs, session=session)
        for rail in reversed(self._rails):
            result = await rail.after(result, session)
        return result
```

**3. SecurityRail**

```python
class SecurityRail(BaseRail):
    BLOCKED_TERMS = ["rm -rf", "DROP TABLE", "eval(", "__import__"]

    async def before(self, inputs, session=None):
        query = inputs.get("query", "")
        for term in self.BLOCKED_TERMS:
            if term.lower() in query.lower():
                return {"result": f"Blocked: dangerous content detected"}
        return inputs
```

**4. Runner 集成**

```python
class Runner:
    rails: RailPipeline = RailPipeline()

    @classmethod
    async def run_agent(cls, agent, inputs, session=None):
        return await cls.rails.run(agent, inputs, session)
```
