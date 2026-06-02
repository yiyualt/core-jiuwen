# coding: utf-8
"""InputGuard — detects dangerous patterns in user input."""


class InputGuard:
    """Checks user input for dangerous content patterns.

    Usage::

        ok, reason = InputGuard.check("What is Python?")  # (True, None)
        ok, reason = InputGuard.check("rm -rf /")         # (False, "Blocked: 'rm -rf'")
    """

    DANGEROUS_PATTERNS: list[str] = [
        "rm -rf",
        "rm -r",
        "drop table",
        "delete from",
        "truncate table",
        "eval(",
        "__import__",
        "os.system",
        "subprocess",
        "exec(",
        "compile(",
        "open(",
    ]

    @classmethod
    def check(cls, text: str) -> tuple[bool, str | None]:
        """Check text for dangerous patterns.

        Args:
            text: The user input to check.

        Returns:
            Tuple of (is_safe: bool, reason: str | None).
        """
        lower = text.lower()
        for pattern in cls.DANGEROUS_PATTERNS:
            if pattern.lower() in lower:
                return False, f"Blocked: dangerous content detected (matched: '{pattern}')"
        return True, None
