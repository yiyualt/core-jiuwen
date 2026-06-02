## ADDED Requirements

### Requirement: DeepAgent is a coding agent
`DeepAgent` SHALL 继承 `ReActAgent`，内置编码工具（bash, read, write）。

#### Scenario: DeepAgent has coding tools
- **WHEN** 创建 DeepAgent(config)
- **THEN** agent 注册了 bash, read, write 工具

### Requirement: Workspace manages file tree
`Workspace` SHALL 提供 list_files, read_file, write_file 方法。

#### Scenario: Read and write files
- **WHEN** workspace.write_file("test.txt", "hello") 然后 workspace.read_file("test.txt")
- **THEN** 返回 "hello"

### Requirement: Factory creates DeepAgent
`create_deep_agent(client, workspace_dir, system_prompt)` SHALL 返回配置好的 DeepAgent。

#### Scenario: Factory with defaults
- **WHEN** 调用 create_deep_agent()
- **THEN** 返回 DeepAgent 实例，使用 OpenAIClient.from_env() 和当前目录
