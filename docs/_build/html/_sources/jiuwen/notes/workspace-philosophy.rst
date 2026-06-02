Workspace: Agent 的安全工位
==============================

``Workspace`` 给 coding agent 限定一个**安全的文件操作边界**。
所有读写操作都在这个目录下进行，越界会被拦截。

为什么需要 Workspace？
-----------------------

没有 Workspace，agent 可以对整个文件系统操作 — 危险且不可控：

.. code-block:: text

    agent: "bash rm -rf /important/data"
    agent: "write /etc/hosts '127.0.0.1 evil.com'"
    agent: "read ~/.ssh/id_rsa"              ← 都可能发生

有 Workspace，所有操作被限制在项目目录内：

.. code-block:: text

    ws = Workspace("/safe/project")

    ws.write_file("src/main.py", ...)         ✓ /safe/project/src/main.py
    ws.read_file("config.json")               ✓ /safe/project/config.json
    ws.list_files("**/*.py")                  ✓ 只列出项目内的文件

    ws.write_file("../etc/passwd", ...)       ✗ ValueError: Path escapes!
    ws.read_file("/etc/hosts")                ✗ ValueError: Path escapes!

架构位置
--------

.. code-block:: text

    jiuwen/harness/
    ├── deep_agent.py        ← 创建 Workspace，注入到工具
    │   ├── bash: cwd = ws.root          ← 命令在项目目录执行
    │   ├── read: ws.read_file(path)     ← 读文件
    │   └── write: ws.write_file(p, c)   ← 写文件
    │
    └── workspace/
        └── workspace.py      ← Workspace 类本身

安全机制
--------

核心在 ``_resolve()`` 方法 — 路径解析后必须仍在根目录下：

.. code-block:: python

    def _resolve(self, path: str) -> Path:
        full = (self.root / path).resolve()        # 解析符号链接
        if not str(full).startswith(str(self.root)): # 必须是子路径
            raise ValueError(f"Path escapes: {path}")
        return full

任何 ``../`` 或符号链接逃逸都会被 ``startswith`` 检查拦截。

API
---

.. code-block:: python

    ws = Workspace("/project")

    # 读
    content = ws.read_file("src/main.py")        # → str
    exists  = ws.exists("README.md")             # → bool

    # 写（自动创建父目录）
    ws.write_file("deep/nested/file.txt", "x")

    # 列
    files = ws.list_files()                      # 所有文件
    py_files = ws.list_files("**/*.py")          # glob 模式

    # 隐藏文件（.__init__、.git、__pycache__）自动被 list_files 过滤

Workspace 与 DeepAgent 的关系
-------------------------------

DeepAgent 内部创建 Workspace，三个工具都基于它：

.. code-block:: python

    class DeepAgent:
        def __init__(self, client, config):
            self._workspace = Workspace(config.workspace_dir)  # 自动创建

            # bash: 命令在 workspace 目录执行
            # read: 调用 self._workspace.read_file()
            # write: 调用 self._workspace.write_file()

默认 workspace_dir = "."，即当前目录。改成指定目录：

.. code-block:: python

    agent = DeepAgent(client, DeepAgentConfig(
        workspace_dir="/home/user/my-project",
    ))

独立使用
--------

Workspace 不依赖 harness，可以独立使用：

.. code-block:: python

    from jiuwen.harness import Workspace

    ws = Workspace("/tmp/scratch")
    ws.write_file("hello.txt", "Hello, World!")
    print(ws.read_file("hello.txt"))
    print(ws.list_files())
