``jiuwen.core.workflow.components``
=====================================

.. module:: jiuwen.core.workflow.components

ComponentAbility
----------------

.. class:: ComponentAbility

   Enum of I/O patterns: ``INVOKE``, ``STREAM``, ``COLLECT``, ``TRANSFORM``.
   Each has ``.name`` and ``.desc`` properties.

WorkflowComponent
-----------------

.. class:: WorkflowComponent

   Base class for user-defined components. Extends :class:`ComponentExecutable`
   and :class:`ComponentComposable`.

   .. method:: async invoke(inputs: dict, **kwargs) -> dict
   .. method:: async stream(inputs: dict, **kwargs) -> AsyncIterator[dict]
   .. method:: async collect(inputs: AsyncIterator[dict], **kwargs) -> dict
   .. method:: async transform(inputs: AsyncIterator[dict], **kwargs) -> AsyncIterator[dict]

Start
-----

.. class:: Start

   Entry point component. Passes inputs through unchanged.

   .. method:: async invoke(inputs: dict, **kwargs) -> dict

End
---

.. class:: End(conf: EndConfig | dict | None = None)

   Exit point component. Wraps outputs, optionally renders a template.

   .. method:: async invoke(inputs: dict, **kwargs) -> dict
   .. method:: async stream(inputs: dict, **kwargs) -> AsyncIterator[dict]

EndConfig
---------

.. class:: EndConfig

   .. attribute:: response_template: str

       Template string using ``{{variable}}`` syntax.
