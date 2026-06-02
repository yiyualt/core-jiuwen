## 三层反馈循环

**Loop 1: CI Fix Loop** (intra-task)
verify 失败 → 注入 CI 错误到 agent → agent 修复 → 重新 verify → 成功或耗尽后回滚

**Loop 2: 任务间经验注入** (intra-session)
implement stage 读取同一 session 中之前任务的经验，避免重复错误

**Loop 3: 跨 session 学习** (inter-session)
LearningsStage 反思整个 session，提取经验写入 JSONL，下次 session 自动加载

## 关键设计

**1. FixLoopController V2**

```python
async def run(self, verify_fn, fix_fn, evaluator=None):
    """Phase 1: agent 修 → 重试 CI; Phase 2: evaluator 审查"""
    for attempt in range(phase1_max):
        result = await verify_fn()
        if result.passed: return FixLoopResult(success=True, ...)
        errors = result.errors
        await fix_fn(errors)  # feed errors back to agent
    # Phase 2: with evaluator
    ...
```

**2. ExperienceStore V2**

- `file_path`: JSONL 文件路径
- `search(query, top_k)`: 关键词匹配 + 时间衰减
- `synthesize(experiences, max_tokens)`: 生成上下文摘要
- `record()`: 写入 JSONL

**3. Session Pipeline**

```
MetaEvolvePipeline.stream(ctx):
  1. assess → plan (在只读快照)
  2. for each task:
       implement → verify(with fix loop) → commit
       on failure: revert + record failure experience
  3. learnings stage (反思 + 写经验)
```
