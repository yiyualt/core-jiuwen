Sys Operation: 安全的系统操作
===============================

提供 Agent 所需的三种系统操作，每种都有超时和安全控制。

与 Workspace / Security 的关系
--------------------------------

三层防护：

.. code-block:: text

    Security              检查"内容是否危险"       InputGuard / OutputGuard
    Workspace             限制"目录范围"           只能访问项目目录
    sys_operation         控制"执行方式"           超时、白名单、子进程隔离

CodeOperator — 执行 Python 代码
--------------------------------

在子进程中执行，自动超时保护：

.. code-block:: python

    from jiuwen.core.sys_operation import CodeOperator

    op = CodeOperator(timeout=5)

    result = await op.execute("print(1 + 1)")
    # OperationResult(success=True, output="2\\n")

    result = await op.execute("while True: pass")  # timeout=0.1
    # OperationResult(success=False, error="timed out")

ShellOperator — 受控 Shell 命令
---------------------------------

白名单限制可执行的命令：

.. code-block:: python

    from jiuwen.core.sys_operation import ShellOperator

    op = ShellOperator(allowed_commands=["ls", "cat", "echo"])

    result = await op.execute("echo hello")   # ✓ allowed
    result = await op.execute("rm -rf /")     # ✗ blocked

FileOperator — 文件 I/O
-------------------------

限制在 base_dir 内的文件操作：

.. code-block:: python

    from jiuwen.core.sys_operation import FileOperator

    op = FileOperator(base_dir="/project")

    op.write("data.txt", "hello world")        # ✓
    content = op.read("data.txt")              # ✓
    op.write("../etc/passwd", "evil")          # ✗ blocked
