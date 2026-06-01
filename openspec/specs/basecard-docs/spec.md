## ADDED Requirements

### Requirement: BaseCard philosophy documentation
文档 SHALL 包含 `docs/jiuwen/notes/basecard-philosophy.rst`，解释 BaseCard 的设计理念、Card/Config 分离模式及其在 agent SDK 中的应用场景。

#### Scenario: Philosophy doc content
- **WHEN** 阅读 basecard-philosophy.rst
- **THEN** 包含 Card/Config 分离的解释
- **THEN** 包含 BaseCard 作为可序列化元数据的角色说明
- **THEN** 包含至少一个使用场景示例

### Requirement: BaseCard example documentation
文档 SHALL 包含 `docs/jiuwen/examples/basecard-example.rst`，提供可运行的 BaseCard 代码示例。

#### Scenario: Example doc content
- **WHEN** 阅读 basecard-example.rst
- **THEN** 包含 BaseCard 基本构造的代码示例
- **THEN** 包含子类化 BaseCard 的代码示例
- **THEN** 包含序列化（model_dump, model_dump_json）的代码示例

### Requirement: BaseCard API reference
文档 SHALL 包含 `docs/jiuwen/api/common.rst`，列出 BaseCard 的公开字段和方法。

#### Scenario: API reference content
- **WHEN** 阅读 api/common.rst
- **THEN** 列出 `id`, `name`, `description` 字段及其类型和默认值
- **THEN** 列出 `tool_info()` 和 `to_str()` 方法及其签名

### Requirement: Getting started tutorial
文档 SHALL 包含 `docs/jiuwen/tutorials/getting-started.rst`，引导新用户完成安装和第一个 BaseCard 使用。

#### Scenario: Getting started content
- **WHEN** 阅读 getting-started.rst
- **THEN** 包含 `pip install -e .` 安装说明
- **THEN** 包含导入 BaseCard 的代码
- **THEN** 包含创建和使用 BaseCard 的最简示例
