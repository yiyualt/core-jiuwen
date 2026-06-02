## Why

Agent 需要执行代码、Shell 命令和文件操作。sys_operation 提供安全的沙箱封装，与 Workspace（限目录）和 Security（限内容）形成三层防护。

## What Changes

- 新增 `jiuwen/core/sys_operation/` 模块
- `base.py`: 操作基类 + 结果类型
- `code.py`: CodeOperator — 安全执行 Python 代码
- `shell.py`: ShellOperator — 受控 Shell 命令
- `fs.py`: FileOperator — 文件读写操作

## Capabilities

### New Capabilities
- `sys-operation`: 代码/Shell/文件操作的安全封装
