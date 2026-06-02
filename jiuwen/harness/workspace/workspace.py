# coding: utf-8
"""Workspace — manages a project directory tree for coding agents.

Provides safe file I/O operations bounded to a root directory.
"""

from pathlib import Path


class Workspace:
    """Manages a coding agent's working directory.

    All file operations are relative to a root directory,
    providing a simple sandbox for file access.

    Usage::

        ws = Workspace("/path/to/project")
        files = ws.list_files()
        content = ws.read_file("src/main.py")
        ws.write_file("output.txt", "Hello, world!")
    """

    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        if not self.root.exists():
            self.root.mkdir(parents=True, exist_ok=True)

    def list_files(self, pattern: str = "*") -> list[str]:
        """List files in the workspace matching a glob pattern.

        Args:
            pattern: Glob pattern relative to workspace root.

        Returns:
            List of relative file paths.
        """
        paths = []
        for p in self.root.rglob(pattern):
            if p.is_file() and not self._is_ignored(p):
                paths.append(str(p.relative_to(self.root)))
        return sorted(paths)

    def read_file(self, path: str) -> str:
        """Read a file from the workspace.

        Args:
            path: Relative path within the workspace.

        Returns:
            File contents as string.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the path escapes the workspace.
        """
        full_path = self._resolve(path)
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return full_path.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> None:
        """Write content to a file in the workspace.

        Creates parent directories if they don't exist.

        Args:
            path: Relative path within the workspace.
            content: Content to write.

        Raises:
            ValueError: If the path escapes the workspace.
        """
        full_path = self._resolve(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

    def exists(self, path: str) -> bool:
        """Check if a file exists in the workspace."""
        return self._resolve(path).exists()

    def _resolve(self, path: str) -> Path:
        """Resolve a relative path against the workspace root.

        Raises ValueError if the path tries to escape the workspace.
        """
        full = (self.root / path).resolve()
        if not str(full).startswith(str(self.root)):
            raise ValueError(f"Path escapes workspace: {path}")
        return full

    @staticmethod
    def _is_ignored(p: Path) -> bool:
        return any(part.startswith(".") for part in p.parts) or "__pycache__" in str(p)
