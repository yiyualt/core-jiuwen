## Context

用 DeepAgent 优化 DeepAgent 的提示词/配置。核心是 Pipeline 概念。

## Decisions

**1. PipelineSpec**

```python
@dataclass
class StageSpec:
    name: str
    description: str
    agent_config: dict  # system_prompt, tools, etc.

@dataclass 
class PipelineSpec:
    name: str
    stages: list[StageSpec]
```

**2. Orchestrator**

```python
class AutoHarnessOrchestrator:
    def __init__(self, client, pipeline=None):
        self._client = client
        self._pipeline = pipeline or default_pipeline()
        self._experience = []

    async def run(self, task: str) -> dict:
        results = []
        for stage in self._pipeline.stages:
            agent = self._create_agent_for_stage(stage)
            result = await agent.run({"query": task})
            self._experience.append({"stage": stage.name, "result": result})
            results.append(result)
        return {"results": results, "experience": self._experience}
```

**3. 标准 Pipeline**

```python
def default_pipeline():
    return PipelineSpec(name="standard", stages=[
        StageSpec("assess", "Analyze the current code"),
        StageSpec("plan", "Create an improvement plan"),
        StageSpec("implement", "Implement the changes"),
        StageSpec("verify", "Verify the changes work"),
    ])
```
