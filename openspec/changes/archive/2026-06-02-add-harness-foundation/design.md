## Context

harness 是 agent-core 的 coding agent 框架。v0.15.0 搭建基础骨架。

## Decisions

**1. 包结构：`jiuwen/harness/` 与 `jiuwen/core/` 平级**

```
jiuwen/
├── __init__.py
├── core/          ← SDK primitives
└── harness/       ← coding agent framework (new)
    ├── __init__.py
    ├── deep_agent.py
    ├── factory.py
    ├── schema/
    │   ├── __init__.py
    │   └── config.py
    └── workspace/
        ├── __init__.py
        └── workspace.py
```

**2. DeepAgent**

```python
class DeepAgent(ReActAgent):
    """A coding agent with built-in tools and system prompt."""

    def __init__(self, config: DeepAgentConfig):
        tools = [
            ToolCard(name="bash", func=self._run_bash, ...),
            ToolCard(name="read", func=self._read_file, ...),
            ToolCard(name="write", func=self._write_file, ...),
        ]
        super().__init__(
            client=config.client,
            tools=tools,
            system_prompt=config.system_prompt,
        )
```

**3. DeepAgentConfig**

```python
class DeepAgentConfig(BaseModel):
    client: LLMClient
    workspace_dir: str = "."
    system_prompt: str = _DEFAULT_CODING_PROMPT
    max_iterations: int = 50
```

**4. Workspace**

```python
class Workspace:
    """Manages a project directory tree."""
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

    def list_files(self) -> list[str]: ...
    def read_file(self, path: str) -> str: ...
    def write_file(self, path: str, content: str) -> None: ...
```

**5. Factory**

```python
def create_deep_agent(
    client: LLMClient | None = None,
    workspace_dir: str = ".",
    system_prompt: str | None = None,
) -> DeepAgent: ...
```

简洁可测试：DeepAgent 用 FakeLLMClient 测试，Workspace 用 tmp_path 测试。
