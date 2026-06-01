## ADDED Requirements

### Requirement: Condition ABC
系统 SHALL 提供 `Condition` 抽象基类，定义 `evaluate(state) -> bool`。

#### Scenario: ExpressionCondition evaluates template
- **WHEN** `ExpressionCondition("{{x}} > 5").evaluate({"x": 10})`
- **THEN** 返回 True

#### Scenario: ExpressionCondition with string comparison
- **WHEN** `ExpressionCondition("{{name}} == 'Bob'").evaluate({"name": "Bob"})`
- **THEN** 返回 True
