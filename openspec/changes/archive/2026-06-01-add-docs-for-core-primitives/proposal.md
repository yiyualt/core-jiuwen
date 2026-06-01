## Why

v0.0.1 的 `BaseCard` 核心原语已经实现并通过 14 个测试，但缺少文档。按照 reproduce 方法论，每个 feature 都需要配套文档（notes/philosophy + examples + API reference），才能让学习者理解设计意图和使用方式。

## What Changes

- 创建 Sphinx 文档骨架（`docs/conf.py`, `docs/index.rst`）
- 新增 `docs/jiuwen/notes/basecard-philosophy.rst` — BaseCard 设计理念（Card/Config 分离模式说明）
- 新增 `docs/jiuwen/examples/basecard-example.rst` — 可运行的 BaseCard 示例代码
- 新增 `docs/jiuwen/api/common.rst` — API 参考文档
- 创建各子目录的 `index.rst` 和 toctree 链接
- 补充 `docs/jiuwen/tutorials/getting-started.rst` — 快速入门教程

## Capabilities

### New Capabilities
- `documentation-infrastructure`: Sphinx 文档骨架、主题配置、构建流程
- `basecard-docs`: BaseCard 的设计理念文档、使用示例、API 参考

### Modified Capabilities
<!-- 无 —— 不修改现有代码行为，仅新增文档 -->

## Impact

- 新增 `docs/` 目录及子目录结构
- 新增 `pyproject.toml` 中的 docs 依赖（sphinx, sphinx-book-theme）
- 不修改 `jiuwen/` 下的任何代码
- 不修改现有测试
