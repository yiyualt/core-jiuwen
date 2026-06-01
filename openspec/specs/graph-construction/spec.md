## ADDED Requirements

### Requirement: Graph builder interface
系统 SHALL 提供 `Graph` 抽象基类，定义 DAG 构建的标准接口。

#### Scenario: Abstract methods defined
- **WHEN** 查看 `Graph` 类
- **THEN** 包含抽象方法 `start_node`, `end_node`, `add_node`, `add_edge`, `add_conditional_edges`, `compile`, `get_nodes`

### Requirement: PregelGraph node management
`PregelGraph` SHALL 支持通过 `add_node` 注册节点，通过 `start_node` 和 `end_node` 标记入口和出口。

#### Scenario: Add a node
- **WHEN** 调用 `graph.add_node("a", my_executable)` 然后 `graph.get_nodes()`
- **THEN** 返回的字典包含键 `"a"`

#### Scenario: Duplicate node raises
- **WHEN** 用相同 ID 调用 `add_node` 两次
- **THEN** 抛出 `ValueError`

#### Scenario: Mark start node
- **WHEN** 调用 `graph.start_node("entry")`
- **THEN** 节点 "entry" 被标记为图入口

#### Scenario: Mark end node
- **WHEN** 调用 `graph.end_node("exit")`
- **THEN** 节点 "exit" 被标记为图出口

### Requirement: PregelGraph edge management
`PregelGraph` SHALL 支持通过 `add_edge` 添加普通边，通过 `add_conditional_edges` 添加条件分支。

#### Scenario: Add simple edge
- **WHEN** 调用 `graph.add_edge("a", "b")`
- **THEN** 边 (a→b) 被添加到图

#### Scenario: Add multi-source edge
- **WHEN** 调用 `graph.add_edge(["a", "b"], "c")`
- **THEN** 边 ([a,b]→c) 被添加到图

#### Scenario: Add conditional edges with router
- **WHEN** 调用 `graph.add_conditional_edges("source", my_router)`
- **THEN** 条件分支被添加到图

### Requirement: Fluent API
`PregelGraph` 的所有构建方法 SHALL 返回 `Self`，支持链式调用。

#### Scenario: Chained construction
- **WHEN** 连续调用 `graph.add_node("a", A).add_node("b", B).add_edge("a", "b")`
- **THEN** 三个调用均有效，图包含两个节点和一条边

### Requirement: Compile to executable graph
`compile()` SHALL 返回 `ExecutableGraph` 实例。

#### Scenario: Compile returns ExecutableGraph
- **WHEN** 调用 `graph.compile()`
- **THEN** 返回的对象是 `ExecutableGraph` 的子类实例
