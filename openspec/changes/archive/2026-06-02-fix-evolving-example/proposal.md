## Why

`docs/jiuwen/examples/evolving-example.rst` 中的示例代码不完整：`SimpleAgent.run()` 是空壳，不使用 LLM；测试用例过于简单无法展示优化器的价值。

## What Changes

- 重写 `evolving-example.rst`，使用完整可运行的代码
- `SimpleAgent` 改为真实的 ReActAgent + FakeLLMClient，展示完整的 失败→优化→成功 流程
- 测试用例包含对默认 agent 有难度的内容

## Impact

- `docs/jiuwen/examples/evolving-example.rst`
