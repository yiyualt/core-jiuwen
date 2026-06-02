Security 示例
=============

组合 InputGuard + OutputGuard
------------------------------

.. code-block:: python

    from jiuwen.core.security import InputGuard, OutputGuard


    def run_safely(user_input: str):
        # 1. 检查输入
        ok, reason = InputGuard.check(user_input)
        if not ok:
            return f"Input rejected: {reason}"

        # 2. 执行 agent（模拟）
        response = f"Agent processed: {user_input}"

        # 3. 检查输出
        ok, found = OutputGuard.check(response)
        if not ok:
            return f"Output blocked: found {found}"

        return response


    print(run_safely("What is Python?"))
    # Agent processed: What is Python?

    print(run_safely("rm -rf /"))
    # Input rejected: Blocked: dangerous content detected

PathSecurity 使用
------------------

.. code-block:: python

    from jiuwen.core.security import PathSecurity


    def read_file_safe(base_dir: str, user_path: str) -> str | None:
        """安全地读取文件。如果路径不安全，返回 None。"""
        safe = PathSecurity.sanitize(base_dir, user_path)
        if safe is None:
            print(f"Blocked: {user_path} escapes {base_dir}")
            return None
        with open(safe) as f:
            return f.read()


    # 正常使用
    content = read_file_safe("/project", "src/main.py")

    # 被拦截
    content = read_file_safe("/project", "../../etc/shadow")
    # Blocked: ../../etc/shadow escapes /project
