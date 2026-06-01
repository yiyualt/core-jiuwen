## Context

v0.0.1 实现了 `BaseCard` 核心原语，现在需要补文档。项目使用 Sphinx + sphinx-book-theme，按照四层文档结构组织：tutorials（教程）、notes（设计理念）、examples（示例）、api（API 参考）。

## Goals / Non-Goals

**Goals:**
- 建立可复用的 Sphinx 文档骨架，后续版本直接在对应目录下新增 `.rst` 文件
- 为 BaseCard 编写设计理念文档，解释 Card/Config 分离模式
- 提供可运行的 BaseCard 使用示例
- 生成 API 参考文档

**Non-Goals:**
- 不修改 jiuwen 包中的代码
- 不创建 v0.0.2+ 模块的文档（那些在各自的 openspec change 中处理）
- 不配置 ReadTheDocs 部署

## Decisions

**1. 文档工具: Sphinx + sphinx-book-theme**
- 理由：与 reproduce 方法论一致，sphinx-book-theme 提供清晰的侧边栏导航
- 替代方案：MkDocs（更简单但不符合 reproduce 规范）

**2. 目录结构: `docs/jiuwen/` 作为项目子目录**
- 理由：支持多项目共存（未来可能有 jiuwen-harness 等）
- 结构：
  ```
  docs/
  ├── conf.py
  ├── index.rst
  └── jiuwen/
      ├── tutorials/
      │   ├── index.rst
      │   └── getting-started.rst
      ├── notes/
      │   ├── index.rst
      │   └── basecard-philosophy.rst
      ├── examples/
      │   ├── index.rst
      │   └── basecard-example.rst
      └── api/
          ├── index.rst
          └── common.rst
  ```

**3. API 文档: 手写 `.rst`（不用 autodoc）**
- 理由：v0.0.1 代码量很小，手写更清晰
- 后续版本可以考虑引入 `autodoc` / `sphinx.ext.autodoc`

## Risks / Trade-offs

- 文档需要随代码演进保持同步 → 每个 openspec change 同时更新文档

## Open Questions

<!-- 无 -->
