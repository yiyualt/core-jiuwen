## Why

已有 Workflow + LLMComponent，但缺少工具调用能力。Tool System 让 Workflow 中可以嵌入任意 Python 函数作为工具组件，是实现 ReActAgent 的前置依赖。

## What Changes

- 新增 `jiuwen/core/foundation/tool.py` — ToolCard（继承 BaseCard）、ToolComponent（WorkflowComponent 子类）
- ToolCard: name + description + parameters（JSON Schema）+ func（可调用对象）
- ToolComponent: 接收 ToolCard，在 invoke 时根据 inputs 调用 func 并返回结果
- 测试使用虚拟工具函数，无需外部依赖
- 文档

## Capabilities

### New Capabilities
- `tool-card`: ToolCard 元数据卡片，描述工具的身份和参数
- `tool-component`: ToolComponent 工作流组件，将 Python 函数包装为 workflow 节点

## Impact

- 新增 `jiuwen/core/foundation/tool.py`
- 更新 `jiuwen/core/foundation/__init__.py`
- 新增对应测试和文档
