## Context

原项目 auto_harness 的核心设计：Pipeline 是顶级抽象，每个 Pipeline 包含多个 Stage。Orchestrator 负责管道选择和执行。

## Decisions

**1. Registry 模式**

```python
class StageRegistry:
    def register(self, name, stage_cls): ...
    def get(self, name) -> BaseStage: ...

class PipelineRegistry:
    def register(self, name, pipeline_cls): ...
    def names(self) -> list[str]: ...
    def get(self, name) -> BasePipeline: ...
```

**2. SessionContext**

```python
@dataclass
class SessionContext:
    orchestrator: Any
    artifacts: dict = {}
    messages: list[str] = []
    def put_artifact(self, key, value): ...
    def get_artifact(self, key): ...
```

**3. BaseStage + StageResult**

```python
class BaseStage(ABC):
    name: str = ""
    @abstractmethod
    async def execute(self, ctx) -> StageResult: ...

@dataclass
class StageResult:
    stage_name: str
    status: str  # "success" | "failed"
    output: str
    artifacts: dict
```

**4. BasePipeline（流式执行）**

```python
class BasePipeline:
    name = ""
    stages: list[BaseStage] = []

    async def stream(self, ctx) -> AsyncIterator:
        for stage in self.stages:
            result = await stage.execute(ctx)
            yield result
            if result.status == "failed" and self._should_retry(stage, result):
                # Fix loop: retry with context from failure
                ...
            ctx.put_artifact(stage.name, result)
```

**5. Fix Loop**

```python
class FixLoopController:
    def __init__(self, max_retries=3): ...
    def should_retry(self, stage_name, result) -> bool: ...
    async def retry(self, stage, ctx, previous_error) -> StageResult: ...
```
