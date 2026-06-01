## ADDED Requirements

### Requirement: ComponentAbility enum
系统 SHALL 定义 `ComponentAbility` 枚举，包含 INVOKE、STREAM、COLLECT、TRANSFORM 四个值，各有 name 和 desc 属性。

#### Scenario: Ability properties
- **WHEN** 访问 `ComponentAbility.INVOKE.name`
- **THEN** 返回 `"invoke"`

### Requirement: WorkflowComponent base class
`WorkflowComponent` SHALL 继承 `ComponentExecutable`，提供 `invoke(inputs, **kwargs) -> dict` 作为主要重写方法。

#### Scenario: Override invoke
- **WHEN** 子类重写 `async def invoke(self, inputs, **kwargs) -> dict`
- **THEN** `await comp.on_invoke(data)` 正确委托到 `invoke`

#### Scenario: Unimplemented invoke raises
- **WHEN** 子类未重写 `invoke`
- **THEN** `await comp.invoke(data)` 抛出 `NotImplementedError`

### Requirement: ComponentConfig and metadata
系统 SHALL 提供 `ComponentConfig` 和 `WorkflowComponentMetadata` 数据类。

#### Scenario: Metadata fields
- **WHEN** 创建 `WorkflowComponentMetadata(node_id="n1", node_type="LLM", node_name="chat")`
- **THEN** 三个字段正确赋值
