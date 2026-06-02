## ADDED Requirements

### Requirement: IntentDetection matches keywords
根据关键词匹配识别用户意图。

#### Scenario: Match greeting intent
- **WHEN** `intents={"greeting": ["hello", "hi"]}`, query="hello there"
- **THEN** 返回 `{"intent": "greeting"}`

#### Scenario: No match returns unknown
- **WHEN** query 不匹配任何关键词
- **THEN** 返回 `{"intent": "unknown", "confidence": 0.0}`
