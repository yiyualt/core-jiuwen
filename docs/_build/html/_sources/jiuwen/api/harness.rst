``jiuwen.harness``
===================

.. module:: jiuwen.harness

DeepAgent
---------

.. class:: DeepAgent(client: LLMClient, config: DeepAgentConfig)

   Coding agent with bash/read/write tools. Extends :class:`ReActAgent`.

   .. attribute:: workspace: Workspace
   .. attribute:: config: DeepAgentConfig

DeepAgentConfig
---------------

.. class:: DeepAgentConfig

   .. attribute:: workspace_dir: str (default ".")
   .. attribute:: system_prompt: str
   .. attribute:: max_iterations: int (default 50)

Workspace
---------

.. class:: Workspace(root_dir: str = ".")

   .. method:: list_files(pattern: str = "*") -> list[str]
   .. method:: read_file(path: str) -> str
   .. method:: write_file(path: str, content: str) -> None
   .. method:: exists(path: str) -> bool

create_deep_agent
-----------------

.. function:: create_deep_agent(client=None, workspace_dir=".", system_prompt=None, max_iterations=50) -> DeepAgent

   Factory with sensible defaults.

PromptBuilder
-------------

.. class:: PromptBuilder(sections: list[BaseSection] | None = None)

   Composes prompt sections.

   .. method:: add_section(section: BaseSection) -> None
   .. method:: build(context: dict | None = None) -> str

BaseSection
-----------

.. class:: BaseSection

   Abstract base for prompt sections.

   .. method:: build(context: dict) -> str

Built-in Sections
-----------------

.. class:: IdentitySection(role: str | None = None)

.. class:: ToolsSection

.. class:: SafetySection

.. class:: WorkspaceSection
