## Context

v0.0.2 引入 Graph 执行引擎，它是工作流系统（v0.0.3+）的运行时核心。参考 agent-core 的 Pregel 模型：节点通过 Channel 通信，执行以 super-step 推进。

## Goals / Non-Goals

**Goals:**
- 定义 Executable 抽象，统一所有可执行节点的接口
- 实现 PregelGraph 构建器，支持 DAG 的流式构建
- 实现 Channel 消息传递（Trigger + Barrier）
- 实现 CompiledGraph 的 super-step 执行循环
- v0.0.2 只实现 invoke 模式（batch in → batch out）

**Non-Goals:**
- 不实现 stream/collect/transform（在后续版本中逐步加入）
- 不实现状态持久化（snapshot/restore）
- 不实现中断恢复（interrupt/resume）
- 不实现子图嵌套

## Decisions

**1. Executable 接口：定义全部 4 种 I/O 模式，但只实现 invoke**

```
Executable[Input, Output]
├── on_invoke(inputs, **kwargs) → Output      ← v0.0.2 实现
├── on_stream(inputs, **kwargs) → AsyncIterator[Output]  ← 抛 NotImplementedError
├── on_collect(inputs, **kwargs) → Output     ← 抛 NotImplementedError
└── on_transform(inputs, **kwargs) → AsyncIterator[Output] ← 抛 NotImplementedError
```

理由：接口完整定义，后续版本只需添加实现，不需要改接口。

**2. PregelGraph：直接存 Executable，不用 Vertex 包装**

v0.0.2 不需要 Vertex 层（它处理 session/tracing/streaming）。节点直接存 `dict[str, Executable]`。

**3. Channel 设计：只保留 Trigger 和 Barrier 两种**

```
TriggerChannel          BarrierChannel
──────┬──────            ──────┬──────
      │                       │
  any → ready              all → ready
  (OR gate)                (AND gate)
```

- Trigger: 简单边 src→tgt，任一 src 触发即可
- Barrier: wait_for_all 边 [a,b]→tgt，全部 src 到达才触发

**4. Super-step 执行循环**

```
Step 0: 种子化 start_nodes → accept(TriggerMessage)
         ┌──────────────────────────────────┐
Step N:  │ 1. 找就绪节点 (channel.is_ready) │
         │ 2. 并发执行 (asyncio.gather)      │
         │ 3. 路由输出到下游 channel         │
         │ 4. step++, 回到 1                │
         └──────────────────────────────────┘
         无就绪节点 → 收集 end_node 输出 → 返回
```

**5. 文件结构：5 个文件，职责分明**

```
graph/
├── executable.py   ← Executable ABC
├── base.py         ← Graph ABC, Router, ExecutableGraph
├── channels.py     ← Channel ABC, TriggerChannel, BarrierChannel
├── graph.py        ← PregelGraph, CompiledGraph
└── __init__.py     ← 导出
```

## Risks / Trade-offs

- Channel 简化版不支持 snapshot/restore → v0.0.2 不可中断恢复
- 无 Vertex 层 → 后续版本需要重构 add_node 来包装 session 逻辑
- 无 wait_for_all 的编译优化 → 简单实现，正确但非最优

## Open Questions

<!-- 无 -->
