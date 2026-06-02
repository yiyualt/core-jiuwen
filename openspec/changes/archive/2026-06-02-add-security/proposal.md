## Why

Agent 可能执行危险操作。Security 模块提供可配置的 guardrails：输入过滤、输出检查、路径安全、命令白名单。

## What Changes

- 新增 `jiuwen/core/security/` 模块
- `input_guard.py`: 输入过滤（危险模式检测）
- `output_guard.py`: 输出检查（敏感信息泄露检测）
- `path_security.py`: 路径安全校验
- 与 core/rails 互补：rails 是中间件框架，security 是具体的安全检查工具

## Capabilities

### New Capabilities
- `security-guardrails`: 输入/输出/路径安全检查
