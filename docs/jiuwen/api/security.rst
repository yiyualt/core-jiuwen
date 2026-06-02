``jiuwen.core.security``
===========================

.. module:: jiuwen.core.security

InputGuard
----------

.. class:: InputGuard

   .. classmethod:: check(text: str) -> tuple[bool, str | None]

      Returns (True, None) if safe, or (False, reason) if dangerous.

   .. attribute:: DANGEROUS_PATTERNS: list[str]

OutputGuard
-----------

.. class:: OutputGuard

   .. classmethod:: check(text: str) -> tuple[bool, list[str]]

      Returns (True, []) if safe, or (False, matches) if sensitive data found.

   .. attribute:: SENSITIVE_PATTERNS: list[str]

PathSecurity
------------

.. class:: PathSecurity

   .. staticmethod:: is_safe(base: str, target: str) -> bool
   .. staticmethod:: sanitize(base: str, target: str) -> str | None
