## Context

安全的三层防护：
1. **Security**: 输入检查（阻止危险模式）
2. **Workspace**: 路径限制（阻止目录逃逸）
3. **sys_operation**: 操作封装（限制执行范围和超时）

## Decisions

**1. OperationResult**

```python
@dataclass
class OperationResult:
    success: bool
    output: str
    error: str | None = None
    exit_code: int = 0
```

**2. CodeOperator**

```python
class CodeOperator:
    def __init__(self, timeout=30, restricted=True):
        ...

    async def execute(self, code: str, globals_dict=None) -> OperationResult:
        # 在子进程中执行，超时杀死
        ...
```

**3. ShellOperator**

```python
class ShellOperator:
    def __init__(self, cwd=".", timeout=30, allowed_commands=None):
        ...

    async def execute(self, command: str) -> OperationResult:
        # 检查白名单，子进程执行
        ...
```

**4. FileOperator**

```python
class FileOperator:
    def __init__(self, base_dir="."):
        ...

    def read(self, path: str) -> OperationResult: ...
    def write(self, path: str, content: str) -> OperationResult: ...
    def list(self, pattern="*") -> OperationResult: ...
```
