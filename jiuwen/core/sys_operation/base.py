# coding: utf-8
"""OperationResult — result container for system operations."""

from dataclasses import dataclass, field


@dataclass
class OperationResult:
    """Result of a system operation (code execution, shell command, file I/O).

    Attributes:
        success: Whether the operation completed successfully.
        output: Standard output from the operation.
        error: Error message if the operation failed.
        exit_code: Process exit code (0 = success).
    """

    success: bool
    output: str = ""
    error: str | None = None
    exit_code: int = 0
