## ADDED Requirements

### Requirement: Executable base class
系统 SHALL 提供 `Executable[Input, Output]` 泛型抽象基类，定义四种 I/O 模式的接口。

#### Scenario: On invoke signature
- **WHEN** 子类实现 `on_invoke(self, inputs: Input, **kwargs) -> Output`
- **THEN** 调用 `await executable.on_invoke(data)` 返回同步结果

#### Scenario: On stream signature
- **WHEN** 子类实现 `on_stream(self, inputs: Input, **kwargs) -> AsyncIterator[Output]`
- **THEN** 调用 `async for chunk in executable.on_stream(data)` 逐块产出

#### Scenario: On collect signature
- **WHEN** 子类实现 `on_collect(self, inputs: AsyncIterator[Input], **kwargs) -> Output`
- **THEN** 调用 `await executable.on_collect(stream)` 收集流并返回聚合结果

#### Scenario: On transform signature
- **WHEN** 子类实现 `on_transform(self, inputs: AsyncIterator[Input], **kwargs) -> AsyncIterator[Output]`
- **THEN** 调用 `async for chunk in executable.on_transform(stream)` 逐块转换

### Requirement: Unimplemented method error
未实现的方法 SHALL 抛出 `NotImplementedError` 并包含类名信息。

#### Scenario: Default on_invoke raises
- **WHEN** 调用未实现 `on_invoke` 的 Executable 子类实例
- **THEN** 抛出 `NotImplementedError`，消息包含类名

### Requirement: GeneralExecutor type alias
系统 SHALL 提供 `GeneralExecutor = Executable[dict[str, Any], dict[str, Any]]` 类型别名。

#### Scenario: Type alias available
- **WHEN** 导入 `GeneralExecutor`
- **THEN** 可直接用于类型注解，等价于 `Executable[dict[str, Any], dict[str, Any]]`
