# coding: utf-8
"""CodeOperator — safe Python code execution in a subprocess."""

import asyncio
import sys
from textwrap import dedent

from jiuwen.core.sys_operation.base import OperationResult


class CodeOperator:
    """Executes Python code in a subprocess with timeout protection.

    Usage::

        op = CodeOperator(timeout=5)
        result = await op.execute("print(1 + 1)")
        # OperationResult(success=True, output="2\\n")
    """

    def __init__(self, timeout: float = 30, restricted: bool = True):
        self._timeout = timeout
        self._restricted = restricted

    async def execute(self, code: str, globals_dict: dict | None = None) -> OperationResult:
        """Execute Python code asynchronously.

        Args:
            code: Python source code string.
            globals_dict: Optional globals dict (unused in subprocess mode).

        Returns:
            OperationResult with output/error.
        """
        code = dedent(code).strip()
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-c", code,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=self._timeout
                )
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                return OperationResult(success=False, error="Code execution timed out")

            output = stdout.decode("utf-8", errors="replace")
            error = stderr.decode("utf-8", errors="replace") or None
            return OperationResult(
                success=proc.returncode == 0,
                output=output,
                error=error,
                exit_code=proc.returncode or 0,
            )
        except Exception as e:
            return OperationResult(success=False, error=str(e))
