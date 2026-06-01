``jiuwen.core.foundation`` — Tool System
==========================================

.. module:: jiuwen.core.foundation
   :no-index:

ToolCard
--------

.. class:: ToolCard

   Metadata card for tools. Inherits from :class:`BaseCard`.

   .. attribute:: parameters: dict | None (default None)

       JSON Schema for tool parameters.

   .. attribute:: func: Callable | None (default None)

       The callable function. **Excluded from serialization**.

   .. method:: tool_info() -> dict

ToolComponent
-------------

.. class:: ToolComponent(card: ToolCard)

   Workflow component wrapping a ToolCard.

   .. attribute:: card: ToolCard

   .. method:: async invoke(inputs: dict, **kwargs) -> dict

       Call the tool function with keyword arguments from inputs.
       Automatically detects sync vs async.
       Returns ``{"output": result}``.
