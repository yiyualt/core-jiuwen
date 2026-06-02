## ADDED Requirements

### Requirement: CodeOperator executes Python safely
`CodeOperator.execute(code)` SHALL 在子进程中执行，支持超时。

#### Scenario: Execute simple code
- **WHEN** `code = "x = 1+1; print(x)"`
- **THEN** 返回 `OperationResult(success=True, output="2\n")`

#### Scenario: Timeout
- **WHEN** `code = "while True: pass"`, timeout=0.1
- **THEN** 返回 `OperationResult(success=False, error="timeout")`

### Requirement: ShellOperator checks command whitelist
`ShellOperator.execute(command)` SHALL 在白名单为空时拒绝，白名单内的命令才允许执行。

#### Scenario: Allowed command
- **WHEN** allowed_commands=["ls", "echo"], command="echo hello"
- **THEN** 返回 `OperationResult(success=True, output="hello\n")`

#### Scenario: Blocked command
- **WHEN** allowed_commands=["ls"], command="rm file"
- **THEN** 返回 `OperationResult(success=False)`

### Requirement: FileOperator provides file I/O
`FileOperator` SHALL 提供 read/write/list 方法。

#### Scenario: Write and read
- **WHEN** write("test.txt", "hello") 然后 read("test.txt")
- **THEN** 返回 "hello"
