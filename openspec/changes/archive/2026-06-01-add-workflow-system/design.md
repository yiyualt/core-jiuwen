## Context

v0.0.1 提供 BaseCard，v0.0.2 提供 PregelGraph。Workflow 是连接二者的桥梁：用 BaseCard 描述身份，用 PregelGraph 执行组件管道。

## Goals / Non-Goals

**Goals:**
- WorkflowCard 继承 BaseCard，增加 version 和 input_params
- Workflow 类封装 PregelGraph，提供组件注册和连接 API
- WorkflowComponent 继承 Executable，简化 invoke 实现
- Start（透传）和 End（可选模板渲染）组件
- 端到端可测试：Start → Custom → End pipeline

**Non-Goals:**
- 不实现 stream/collect/transform（沿用 Executable 的默认抛错）
- 不实现 Runner（v0.0.7）
- 不实现 LLMComponent（v0.0.5-6）
- 不实现条件分支组件（v0.0.11）

## Decisions

**1. 合并 v0.0.3 + v0.0.4**

Workflow 需要至少 Start/End 才能端到端测试，分开发布会导致中间状态不可验证。合并后一个 change 交付完整可用的 pipeline 系统。

**2. Workflow 封装 PregelGraph，不继承**

```
Workflow
├── _card: WorkflowCard          ← 身份
├── _graph: PregelGraph          ← 执行引擎
├── _components: dict[str, Any]  ← 组件注册表
└── invoke(inputs) → WorkflowOutput
```

接口设计：
```
set_start_comp(id, comp, inputs_schema) → Self
add_workflow_comp(id, comp, inputs_schema) → Self
set_end_comp(id, comp, inputs_schema) → Self
add_connection(src, tgt) → Self
add_conditional_connection(src, router) → Self
invoke(inputs) → WorkflowOutput
```

**3. 组件层次结构**

```
Executable (v0.0.2)
  └── ComponentExecutable   ← 新增：委托 on_invoke → invoke
        └── WorkflowComponent ← 新增：用户继承的基类
              ├── Start       ← 新增
              └── End         ← 新增（+ EndConfig）
```

**4. End 组件模板语法**

使用 Python `string.Template`，`{{var}}` → `$var`：
```python
End({"responseTemplate": "结果是: {{output}}"})
# 输入 {"output": "hello"} → 输出 {"response": "结果是: hello"}
```

**5. 重复组件处理**

同一个组件可能既是 Start 又是 End。Workflow 的 set_start_comp / set_end_comp 会检测是否已注册，已注册则跳过 add_node 只做标记。

## Risks / Trade-offs

- End 的模板渲染使用 Python string.Template（简单但有限）→ 后续可替换为 Jinja2
- Workflow.invoke 直接调用 compiled._invoke()（绕过 session 参数）→ 等 v0.0.7 Runner 引入后重构

## Open Questions

<!-- 无 -->
