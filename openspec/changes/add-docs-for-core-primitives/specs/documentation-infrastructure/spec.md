## ADDED Requirements

### Requirement: Sphinx documentation skeleton
项目 SHALL 提供基于 Sphinx + sphinx-book-theme 的文档骨架，支持 `sphinx-build -b html` 构建无错误的 HTML 输出。

#### Scenario: Build succeeds
- **WHEN** 执行 `sphinx-build -b html docs/ docs/_build/html`
- **THEN** 构建成功完成，无 Sphinx 警告或错误
- **THEN** 生成 `docs/_build/html/index.html` 作为首页

### Requirement: Four-layer documentation structure
文档 SHALL 按四层结构组织：tutorials（教程）、notes（设计理念）、examples（示例）、api（API 参考），每层有独立的 `index.rst` 和 toctree。

#### Scenario: Navigation structure
- **WHEN** 访问文档首页
- **THEN** 侧边栏显示 tutorials, notes, examples, api 四个顶层导航项

### Requirement: docs dependency in pyproject.toml
项目的 `pyproject.toml` SHALL 包含 docs 可选依赖组，包含 sphinx 和 sphinx-book-theme。

#### Scenario: Install docs dependencies
- **WHEN** 执行 `uv sync --group docs`
- **THEN** sphinx 和 sphinx-book-theme 被安装
