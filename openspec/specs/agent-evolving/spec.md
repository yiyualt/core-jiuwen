## ADDED Requirements

### Requirement: Case defines test input/output
`Case` SHALL 定义输入和期望输出，用于评估 agent。

#### Scenario: Case construction
- **WHEN** 创建 `Case(input={"query": "2+2"}, expected="4")`
- **THEN** case.input 和 case.expected 正确存储

### Requirement: Evaluator scores agent
`Evaluator.evaluate(agent)` SHALL 对每个 case 运行 agent，计算准确率。

#### Scenario: Perfect score
- **WHEN** agent 在所有 case 上输出符合期望
- **THEN** 返回 score=1.0

#### Scenario: Partial score
- **WHEN** agent 在一半 case 上正确
- **THEN** 返回 score=0.5

### Requirement: Optimizer generates improved prompt
`Optimizer.optimize(prompt, failures)` SHALL 基于失败案例生成改进的提示词。

#### Scenario: Generate better prompt
- **WHEN** 提供当前提示词和失败案例列表
- **THEN** LLM 返回新的改进提示词

### Requirement: Trainer iterates to convergence
`Trainer.train(agent)` SHALL 迭代 evaluate → optimize 直到收敛。

#### Scenario: Training loop
- **WHEN** 初始 agent 得分 0.5，optimizer 生成更好的提示词
- **THEN** 最终返回 best_prompt 和 best_score>=0.5
