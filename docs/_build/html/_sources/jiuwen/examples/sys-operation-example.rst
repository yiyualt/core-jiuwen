Sys Operation 示例
===================

代码执行
---------

.. code-block:: python

    import asyncio
    from jiuwen.core.sys_operation import CodeOperator


    async def main():
        op = CodeOperator(timeout=5)

        # 正常执行
        r = await op.execute("print(sum(range(10)))")
        print(r.success, r.output)  # True, "45\\n"

        # 错误代码
        r = await op.execute("1/0")
        print(r.success, r.error)   # False, ZeroDivisionError...

    asyncio.run(main())

Shell 白名单
--------------

.. code-block:: python

    import asyncio
    from jiuwen.core.sys_operation import ShellOperator


    async def main():
        op = ShellOperator(allowed_commands=["ls", "echo", "wc"])

        # 允许
        r = await op.execute("ls -la")
        print(r.success)  # True

        # 拒绝
        r = await op.execute("cat /etc/passwd")
        print(r.error)    # "Command 'cat' is not allowed"

    asyncio.run(main())

文件操作
---------

.. code-block:: python

    from jiuwen.core.sys_operation import FileOperator
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        op = FileOperator(tmp)
        op.write("hello.py", "print('hi')")
        r = op.read("hello.py")
        print(r.output)  # print('hi')
