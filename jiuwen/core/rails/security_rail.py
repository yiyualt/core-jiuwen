# coding: utf-8
"""SecurityRail — blocks dangerous content in agent inputs."""

from jiuwen.core.rails.base import BaseRail


class SecurityRail(BaseRail):
    """A rail that checks inputs for dangerous content.

    If a blocked pattern is found in the user's query, the agent
    is short-circuited and a safe response is returned instead.

    Usage::

        rail = SecurityRail()
        result = await rail.before({"query": "DROP TABLE users"})
        # result = {"result": "Blocked: dangerous content detected"}
    """

    BLOCKED_TERMS: list[str] = [
        "rm -rf",
        "rm -r",
        "drop table",
        "delete from",
        "eval(",
        "__import__",
        "os.system",
        "subprocess",
    ]

    def __init__(self, blocked_terms: list[str] | None = None):
        """Initialize with optional custom blocked terms.

        Args:
            blocked_terms: Custom list of blocked patterns.
                          If None, uses the default BLOCKED_TERMS.
        """
        self._blocked = blocked_terms or list(self.BLOCKED_TERMS)

    async def before(self, inputs: dict, session=None) -> dict:
        """Check inputs for dangerous content.

        Args:
            inputs: Agent inputs dict (must contain "query" key).
            session: Optional session (unused).

        Returns:
            Original inputs if safe, or {"result": "Blocked: ..."} if dangerous.
        """
        query = inputs.get("query", "").lower()
        for term in self._blocked:
            if term.lower() in query:
                return {"result": f"Blocked: dangerous content detected (matched: '{term}')"}
        return inputs
