Security: Guardrails 安全层
==============================

Security 模块提供三个独立的检查工具，保护 agent 的输入、输出和文件访问。

与 Rails 的关系
----------------

.. code-block:: text

    core/rails/          ← 中间件框架（编排）
    core/security/       ← 安全检查工具（执行）

    Rails 用 Security 做具体检查：
    ┌──────────────┐
    │ SecurityRail │──→ InputGuard.check(inputs["query"])
    └──────────────┘

两者可以独立使用，也可以组合。

InputGuard — 输入过滤
----------------------

拦截危险命令和代码注入：

.. code-block:: python

    from jiuwen.core.security import InputGuard

    ok, _ = InputGuard.check("What is Python?")   # (True, None)
    ok, _ = InputGuard.check("rm -rf /tmp")       # (False, "Blocked: 'rm -rf'")
    ok, _ = InputGuard.check("DROP TABLE users")  # (False, "Blocked: 'drop table'")

OutputGuard — 输出检查
-----------------------

检测 agent 输出是否泄露敏感信息：

.. code-block:: python

    from jiuwen.core.security import OutputGuard

    ok, _ = OutputGuard.check("Here is your code.")  # (True, [])
    ok, _ = OutputGuard.check("API key: sk-abc...")  # (False, ["sk-abc..."])

PathSecurity — 路径安全
-------------------------

确保文件操作在允许的目录内：

.. code-block:: python

    from jiuwen.core.security import PathSecurity

    PathSecurity.is_safe("/project", "src/main.py")   # True
    PathSecurity.is_safe("/project", "../etc/passwd")  # False
