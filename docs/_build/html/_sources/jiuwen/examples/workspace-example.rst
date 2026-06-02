Workspace 示例
================

基础用法
--------

.. code-block:: python

    from jiuwen.harness import Workspace

    # 创建 workspace（自动创建目录）
    ws = Workspace("/tmp/my-project")

    # 写文件
    ws.write_file("README.md", "# My Project\\n\\nHello, World!")
    ws.write_file("src/utils.py", "def greet():\\n    return 'hi'")

    # 读文件
    print(ws.read_file("README.md"))

    # 检查存在
    assert ws.exists("src/utils.py")
    assert not ws.exists("nonexistent.py")

    # 列出文件
    all_files = ws.list_files()
    py_files  = ws.list_files("**/*.py")
    print(py_files)  # ['src/utils.py']

安全边界
--------

.. code-block:: python

    from jiuwen.harness import Workspace

    ws = Workspace("/safe/dir")

    # 正常操作 — 都在 workspace 内
    ws.write_file("data.txt", "ok")
    ws.write_file("sub/deep/file.txt", "ok")

    # 逃逸尝试 — 全部被拦截
    try:
        ws.write_file("../../etc/passwd", "evil")
    except ValueError as e:
        print(e)  # "Path escapes workspace: ../../etc/passwd"

    try:
        ws.read_file("/etc/hosts")
    except ValueError as e:
        print(e)  # "Path escapes workspace: /etc/hosts"

隐藏文件过滤
-------------

.. code-block:: python

    from jiuwen.harness import Workspace
    from pathlib import Path

    ws = Workspace("/tmp/test-ws")

    ws.write_file("normal.py", "x")
    ws.write_file(".hidden.py", "x")           # 以 . 开头
    Path(ws.root, "__pycache__/cached.py").mkdir(parents=True)
    Path(ws.root, "__pycache__/cached.py").write_text("x")

    files = ws.list_files()
    print(files)  # ['normal.py'] — 只有这一个

集成到 Agent
-------------

.. code-block:: python

    import asyncio
    from tests.conftest import FakeLLMClient
    from jiuwen.harness import DeepAgent, DeepAgentConfig
    from tempfile import TemporaryDirectory


    async def main():
        with TemporaryDirectory() as tmp:
            agent = DeepAgent(
                FakeLLMClient([
                    "Action: write(path='hello.py', content='print(42)')",
                    "Final Answer: File created.",
                ]),
                DeepAgentConfig(workspace_dir=tmp),
            )

            result = await agent.run({"query": "Create hello.py"})
            print(result["result"])  # "File created."

            with open(f"{tmp}/hello.py") as f:
                print(f.read())  # print(42)

    asyncio.run(main())
