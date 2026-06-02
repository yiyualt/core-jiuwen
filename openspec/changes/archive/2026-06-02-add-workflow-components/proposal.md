## Why

Workflow 组件库目前只有 Start、End、LLM、Branch。回填 4 个缺失的组件类型，丰富 pipeline 构建能力。

## What Changes

- `QuestionerComponent`: 输入不明确时追问用户
- `IntentDetectionComponent`: 识别用户意图并路由
- `HTTPRequestComponent`: 发起 HTTP 请求
- `LoopComponent`: 循环执行（指定次数或直到条件满足）

## Capabilities

### New Capabilities
- `questioner-component`
- `intent-detection-component`
- `http-component`
- `loop-component`
