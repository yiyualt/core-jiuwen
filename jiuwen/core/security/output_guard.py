# coding: utf-8
"""OutputGuard — detects sensitive information in agent outputs."""

import re


class OutputGuard:
    """Checks agent output for leaked sensitive information.

    Usage::

        ok, found = OutputGuard.check("Here is your code.")
        # (True, [])

        ok, found = OutputGuard.check("API key: sk-abc123def456ghi789jkl012mnopqrstuv")
        # (False, ["sk-..."])
    """

    SENSITIVE_PATTERNS: list[str] = [
        r"\b\d{13,19}\b",                      # Credit card numbers (13-19 digits)
        r"sk-[a-zA-Z0-9]{20,}",                # OpenAI API keys
        r"Bearer\s+[a-zA-Z0-9\-_.]{20,}",      # Bearer tokens
        r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*\S+",  # Key=value secrets
    ]

    @classmethod
    def check(cls, text: str) -> tuple[bool, list[str]]:
        """Check text for sensitive patterns.

        Args:
            text: The output text to check.

        Returns:
            Tuple of (is_safe: bool, matched_patterns: list[str]).
        """
        found = []
        for pattern in cls.SENSITIVE_PATTERNS:
            matches = re.findall(pattern, text)
            found.extend(matches)
        return len(found) == 0, found
