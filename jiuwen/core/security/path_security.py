# coding: utf-8
"""PathSecurity — validates file paths are within a safe base directory."""

from pathlib import Path


class PathSecurity:
    """Validates that file paths don't escape a base directory.

    Usage::

        PathSecurity.is_safe("/project", "src/main.py")     # True
        PathSecurity.is_safe("/project", "../etc/passwd")   # False
    """

    @staticmethod
    def is_safe(base: str, target: str) -> bool:
        """Check if target path stays within base directory.

        Args:
            base: The base directory path.
            target: The target path to check (can be relative).

        Returns:
            True if target resolves within base, False otherwise.
        """
        try:
            base_path = Path(base).resolve()
            target_path = (base_path / target).resolve()
            return str(target_path).startswith(str(base_path))
        except Exception:
            return False

    @staticmethod
    def sanitize(base: str, target: str) -> str | None:
        """If safe, return the resolved path. Otherwise None.

        Args:
            base: Base directory.
            target: Target path.

        Returns:
            Resolved absolute path string, or None if unsafe.
        """
        if PathSecurity.is_safe(base, target):
            return str((Path(base).resolve() / target).resolve())
        return None
