``jiuwen.core.graph``
======================

.. module:: jiuwen.core.graph

Executable
----------

.. class:: Executable(Generic[Input, Output])

   Abstract base class for all invokable graph nodes.

   **Methods**

   .. method:: async on_invoke(inputs: Input, **kwargs) -> Output
      :abstractmethod:

      Execute with batch input, return batch output.

   .. method:: async on_stream(inputs: Input, **kwargs) -> AsyncIterator[Output]
      :abstractmethod:

      Execute with batch input, yield streaming output.

   .. method:: async on_collect(inputs: AsyncIterator[Input], **kwargs) -> Output
      :abstractmethod:

      Collect streaming input, return batch output.

   .. method:: async on_transform(inputs: AsyncIterator[Input], **kwargs) -> AsyncIterator[Output]
      :abstractmethod:

      Transform streaming input to streaming output.

   .. method:: skip_trace() -> bool

   .. method:: post_commit() -> bool

   .. method:: component_type() -> str

PregelGraph
-----------

.. class:: PregelGraph()

   Concrete graph builder. Construct DAGs with nodes and edges.

   .. method:: add_node(node_id: str, node: Executable, *, wait_for_all: bool = False) -> Self
   .. method:: add_edge(source_node_id: str | list[str], target_node_id: str) -> Self
   .. method:: add_conditional_edges(source_node_id: str, router: Router) -> Self
   .. method:: start_node(node_id: str) -> Self
   .. method:: end_node(node_id: str) -> Self
   .. method:: compile(session=None, **kwargs) -> ExecutableGraph
   .. method:: get_nodes() -> dict

Channels
--------

.. class:: Channel

   Abstract base for message channels.

   .. method:: is_ready() -> bool
   .. method:: accept(message) -> bool
   .. method:: consume() -> None
   .. method:: snapshot() -> Any
   .. method:: restore(state) -> None

.. class:: TriggerChannel(node_name: str)

   Fires when any message arrives (OR gate).

.. class:: BarrierChannel(node_name: str, expected_senders: Set[str])

   Fires when all expected senders have arrived (AND gate).

Types
-----

.. data:: Router
   :type: Union[Callable[..., Hashable | Sequence[Hashable]], Callable[..., Awaitable[Hashable | Sequence[Hashable]]]]

.. data:: GeneralExecutor
   :type: Executable[dict[str, Any], dict[str, Any]]
