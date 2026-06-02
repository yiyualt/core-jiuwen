## ADDED Requirements

### Requirement: InputGuard detects dangerous input
`InputGuard.check(text)` SHALL 返回 `(True, None)` 或 `(False, reason)`。

#### Scenario: Blocks rm -rf
- **WHEN** `text = "please rm -rf /"`
- **THEN** 返回 `(False, "Blocked: 'rm -rf'")`

#### Scenario: Passes safe input
- **WHEN** `text = "What is Python?"`
- **THEN** 返回 `(True, None)`

### Requirement: OutputGuard detects sensitive data
`OutputGuard.check(text)` SHALL 检测信用卡号、API key 等敏感信息。

#### Scenario: Detects API key
- **WHEN** text 包含 `sk-` 开头的长字符串
- **THEN** 返回 `(False, ["sk-..."])`

#### Scenario: Passes normal output
- **WHEN** text 为普通回答
- **THEN** 返回 `(True, [])`

### Requirement: PathSecurity validates paths
`PathSecurity.is_safe(base, target)` SHALL 校验 target 是否在 base 之内。

#### Scenario: Safe path
- **WHEN** `base="/a", target="b/c"`
- **THEN** 返回 True

#### Scenario: Unsafe escape
- **WHEN** `base="/a", target="../etc/passwd"`
- **THEN** 返回 False
