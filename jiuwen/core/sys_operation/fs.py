# coding: utf-8
"""FileOperator — safe file read/write/list operations."""

from pathlib import Path
from jiuwen.core.sys_operation.base import OperationResult


class FileOperator:
    """Provides file I/O operations within a base directory.

    Usage::

        op = FileOperator(base_dir="/tmp/work")
        result = op.write("test.txt", "hello")
        # OperationResult(success=True, output="Wrote test.txt")
        content = op.read("test.txt")
        # OperationResult(success=True, output="hello")
    """

    def __init__(self, base_dir: str = "."):
        self._base = Path(base_dir).resolve()
        self._base.mkdir(parents=True, exist_ok=True)

    def read(self, path: str) -> OperationResult:
        """Read a file relative to base_dir."""
        try:
            full = self._resolve(path)
            content = full.read_text(encoding="utf-8")
            return OperationResult(success=True, output=content)
        except ValueError as e:
            return OperationResult(success=False, error=str(e))
        except FileNotFoundError:
            return OperationResult(success=False, error=f"File not found: {path}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def write(self, path: str, content: str) -> OperationResult:
        """Write content to a file relative to base_dir."""
        try:
            full = self._resolve(path)
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(content, encoding="utf-8")
            return OperationResult(success=True, output=f"Wrote {path}")
        except ValueError as e:
            return OperationResult(success=False, error=str(e))
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def list(self, pattern: str = "*") -> OperationResult:
        """List files matching a glob pattern."""
        try:
            paths = sorted(
                str(p.relative_to(self._base))
                for p in self._base.rglob(pattern)
                if p.is_file()
            )
            return OperationResult(success=True, output="\n".join(paths))
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def _resolve(self, path: str) -> Path:
        full = (self._base / path).resolve()
        if not str(full).startswith(str(self._base)):
            raise ValueError(f"Path escapes base directory: {path}")
        return full
