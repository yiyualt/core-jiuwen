## Why

DeepAgent 当前使用一个硬编码字符串作为 system prompt。Harness Prompts 提供分层、可组合的提示词构建系统，每个 section 独立可测、可按需组合。

## What Changes

- 新增 `jiuwen/harness/prompts/` — PromptBuilder + BaseSection + built-in sections
- IdentitySection: agent 身份
- ToolsSection: 工具使用说明
- SafetySection: 安全规则
- WorkspaceSection: 工作目录上下文
- DeepAgent 集成 PromptBuilder

## Capabilities

### New Capabilities
- `harness-prompts`: 分层提示词构建系统
