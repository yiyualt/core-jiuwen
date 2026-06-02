``jiuwen.core.sys_operation``
===============================

.. module:: jiuwen.core.sys_operation

OperationResult
---------------

.. class:: OperationResult

   .. attribute:: success: bool
   .. attribute:: output: str
   .. attribute:: error: str | None
   .. attribute:: exit_code: int

CodeOperator
------------

.. class:: CodeOperator(timeout: float = 30)

   .. method:: async execute(code: str) -> OperationResult

ShellOperator
-------------

.. class:: ShellOperator(cwd: str = ".", timeout: float = 30, allowed_commands: list[str] | None = None)

   .. method:: async execute(command: str) -> OperationResult

FileOperator
------------

.. class:: FileOperator(base_dir: str = ".")

   .. method:: read(path: str) -> OperationResult
   .. method:: write(path: str, content: str) -> OperationResult
   .. method:: list(pattern: str = "*") -> OperationResult
