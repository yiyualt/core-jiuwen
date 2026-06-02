## Context

与 core/rails 的关系：rails 是框架，security 是工具。SecurityGuard 可以被 Rails 使用，也可以独立调用。

## Decisions

**1. InputGuard**

```python
class InputGuard:
    DANGEROUS = ["rm -rf", "DROP TABLE", "eval(", "__import__", "os.system", "subprocess"]

    @classmethod
    def check(cls, text: str) -> tuple[bool, str | None]:
        for pattern in cls.DANGEROUS:
            if pattern.lower() in text.lower():
                return False, f"Blocked: '{pattern}'"
        return True, None
```

**2. OutputGuard**

```python
class OutputGuard:
    SENSITIVE = [r'\b\d{16}\b', r'sk-[a-zA-Z0-9]{32,}', r'Bearer\s+[a-zA-Z0-9\-_\.]+']

    @classmethod
    def check(cls, text: str) -> tuple[bool, list[str]]:
        found = [p for p in cls.SENSITIVE if re.search(p, text)]
        return len(found) == 0, found
```

**3. PathSecurity**

```python
class PathSecurity:
    @staticmethod
    def is_safe(base: str, target: str) -> bool:
        return Path(base, target).resolve().is_relative_to(Path(base).resolve())
```
