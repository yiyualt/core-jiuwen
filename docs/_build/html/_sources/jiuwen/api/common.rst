``jiuwen.core.common``
========================

.. module:: jiuwen.core.common

BaseCard
--------

.. class:: BaseCard

   Base class for all metadata cards in jiuwen. Inherits from
   :class:`pydantic.BaseModel`.

   **Fields**

   .. attribute:: id: str

      Unique identifier, auto-generated UUID hex string (32 chars).
      Can be overridden at construction.

   .. attribute:: name: str

      Human-readable name. Should be unique within its namespace.
      Default: ``""``.

   .. attribute:: description: str

      Description of the card's purpose, capabilities, and use cases.
      Default: ``""``.

   **Methods**

   .. method:: tool_info()

      Return tool-compatible metadata for this card. Override in
      subclasses to provide structured tool descriptions.

      :rtype: ``dict`` or ``None``

   .. method:: to_str() -> str

      Return a compact string representation in ``id=...,name=...`` format.

      :rtype: ``str``
