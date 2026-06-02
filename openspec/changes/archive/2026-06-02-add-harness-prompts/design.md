## Context

将大型 system prompt 拆分为可组合的 sections。

## Decisions

**1. BaseSection ABC**

```python
class BaseSection(ABC):
    @abstractmethod
    def build(self, context: dict) -> str: ...
```

**2. 内置 Sections**

- IdentitySection: "You are an expert software engineer."
- ToolsSection: 列出可用工具及使用方法
- SafetySection: "Never delete files without asking."
- WorkspaceSection: 工作目录信息

**3. PromptBuilder**

```python
class PromptBuilder:
    def __init__(self, sections=None):
        self._sections = sections or [IdentitySection(), ToolsSection(), SafetySection()]

    def build(self, context=None) -> str:
        return "\n\n".join(s.build(context or {}) for s in self._sections)
```

**4. DeepAgent 集成**

```python
class DeepAgent:
    def __init__(self, client, config, prompt_builder=None):
        builder = prompt_builder or default_builder
        system_prompt = builder.build({"workspace": str(self._workspace.root)})
```
