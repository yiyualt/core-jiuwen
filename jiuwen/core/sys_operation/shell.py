# coding: utf-8
"""ShellOperator — controlled shell command execution."""

import asyncio

from jiuwen.core.sys_operation.base import OperationResult


class ShellOperator:
    """Executes shell commands with optional whitelist protection.

    Usage::

        op = ShellOperator(allowed_commands=["ls", "echo", "cat"])
        result = await op.execute("echo hello")
        # OperationResult(success=True, output="hello\\n")

        result = await op.execute("rm -rf /")
        # OperationResult(success=False, error="Command 'rm' is not allowed")
    """

    def __init__(
        self,
        cwd: str = ".",
        timeout: float = 30,
        allowed_commands: list[str] | None = None,
    ):
        self._cwd = cwd
        self._timeout = timeout
        self._allowed = allowed_commands or []

    async def execute(self, command: str) -> OperationResult:
        """Execute a shell command.

        Args:
            command: Shell command string.

        Returns:
            OperationResult with output/error.
        """
        cmd_name = command.strip().split()[0] if command.strip() else ""

        if self._allowed and cmd_name not in self._allowed:
            return OperationResult(
                success=False,
                error=f"Command '{cmd_name}' is not allowed. Allowed: {self._allowed}",
            )

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                cwd=self._cwd,
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
                return OperationResult(success=False, error="Command timed out")

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
