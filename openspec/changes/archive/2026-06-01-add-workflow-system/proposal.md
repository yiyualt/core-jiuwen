## Why

v0.0.1 提供了身份标识（BaseCard），v0.0.2 提供了执行引擎（PregelGraph）。现在需要将它们连接成完整的 Workflow 系统：用户可以用 Workflow 把组件串成 pipeline 并执行。合并 v0.0.3 和 v0.0.4，一次性交付可端到端测试的 Workflow + 基础组件。

## What Changes

- 新增 `jiuwen/core/workflow/` 模块
- `base.py`: WorkflowCard（继承 BaseCard）、WorkflowExecutionState 枚举、WorkflowOutput 容器、generate_workflow_key 工具函数
- `workflow.py`: Workflow 类，封装 PregelGraph，提供 set_start_comp / add_workflow_comp / set_end_comp / add_connection 接口
- `components/`: 组件系统
  - `base.py`: ComponentAbility 枚举、ComponentConfig、WorkflowComponentMetadata
  - `component.py`: WorkflowComponent 基类（继承 Executable）+ ComponentComposable mixin
  - `flow/start_comp.py`: Start 组件（透传输入）
  - `flow/end_comp.py`: End 组件 + EndConfig（可选模板渲染）
- 测试：workflow base + workflow + components 各一个测试文件
- 文档：workflow 和 components 的 notes + examples + api

## Capabilities

### New Capabilities
- `workflow-base-types`: WorkflowCard、WorkflowExecutionState、WorkflowOutput、generate_workflow_key
- `workflow-orchestration`: Workflow 类，组件的注册、连接、编译和执行
- `component-system`: WorkflowComponent 基类、ComponentAbility、ComponentConfig
- `start-end-components`: Start 和 End 组件，支持模板渲染

### Modified Capabilities
<!-- 无 -->

## Impact

- 新增 `jiuwen/core/workflow/` 包
- 新增 `tests/unit_tests/core/workflow/` 测试
- 新增 `docs/jiuwen/notes/` 2 个设计文档
- 新增 `docs/jiuwen/examples/` 2 个示例
- 新增 `docs/jiuwen/api/` 2 个 API 参考
- 不修改 v0.0.1 和 v0.0.2 的代码
