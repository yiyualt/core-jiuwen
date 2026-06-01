## Why

工作流（Workflow）需要一个执行引擎来调度组件按 DAG 图顺序运行。Graph 引擎是连接"组件"和"工作流"的桥梁——没有它，组件只是孤立的函数，无法组成处理管道。

## What Changes

- 新增 `jiuwen/core/graph/` 模块（5 个文件）
- `executable.py`: Executable 抽象基类，定义 4 种 I/O 模式（invoke/stream/collect/transform）
- `base.py`: Graph 构建器接口（ABC）+ Router 类型别名 + ExecutableGraph 编译形态
- `channels.py`: Channel 消息传递系统（TriggerChannel + BarrierChannel）
- `graph.py`: PregelGraph 具体实现 + CompiledGraph 执行器（super-step 循环）
- 测试：executable、channels、graph 各一个测试文件
- 文档：为每个模块创建 notes + examples + api 文档

## Capabilities

### New Capabilities
- `executable-abstraction`: 定义 Executable 抽象基类，支持 invoke/stream/collect/transform 四种 I/O 模式
- `graph-construction`: Graph 构建器接口 + PregelGraph 具体实现，支持 add_node/add_edge/start_node/end_node/compile 的流式 API
- `channel-messaging`: Channel 消息传递系统，TriggerChannel（或门）和 BarrierChannel（与门）两种语义
- `graph-execution`: CompiledGraph 执行器，Pregel 风格的 super-step 循环：就绪检测 → 并发执行 → 路由输出 → 重复

### Modified Capabilities
<!-- 无 —— 不修改 v0.0.1 代码 -->

## Impact

- 新增 `jiuwen/core/graph/` 包
- 新增 `tests/unit_tests/core/graph/` 测试
- 新增 `docs/jiuwen/notes/graph-*.rst` 设计文档
- 新增 `docs/jiuwen/examples/graph-*.rst` 示例
- 新增 `docs/jiuwen/api/graph.rst` API 参考
- 不修改 v0.0.1 的 `jiuwen/core/common/base.py`
