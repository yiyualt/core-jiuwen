Auto Harness: 自动优化框架的实现
===================================

auto_harness 用 **DeepAgent 优化 DeepAgent 自身**。它是 jiuwen 的"元框架"。

核心思想
--------

手工写 agent 提示词很难 — 太短不够精确，太长浪费 token。auto_harness
把优化过程变成**标准化的多阶段管道**，每个阶段用专门的 agent 完成。

.. code-block:: text

    输入: "优化数据库查询性能"
    │
    ▼
    ┌──────────────────────────────────────────────────────┐
    │  Pipeline: assess → plan → implement → verify       │
    │                                                      │
    │  Stage 1 "assess":                                   │
    │    Agent(system_prompt="你是代码审查员")               │
    │    → 分析代码，找出性能瓶颈                            │
    │                                                      │
    │  Stage 2 "plan":                                     │
    │    Agent(system_prompt="你是架构师")                   │
    │    → 基于评估结果制定优化方案                           │
    │                                                      │
    │  Stage 3 "implement":                                │
    │    Agent(system_prompt="你是开发者")                   │
    │    → 执行优化方案，修改代码                             │
    │                                                      │
    │  Stage 4 "verify":                                   │
    │    Agent(system_prompt="你是测试员")                   │
    │    → 验证修改是否有效                                  │
    └──────────────────────────────────────────────────────┘
    │
    ▼
    输出: 每阶段的执行结果 + 经验记录

实现细节
--------

**PipelineSpec** 定义管道的结构：

.. code-block:: python

    @dataclass
    class StageSpec:
        name: str             # 阶段名称
        description: str      # 阶段描述
        system_prompt: str    # 该阶段 agent 的系统提示词

    @dataclass
    class PipelineSpec:
        name: str
        stages: list[StageSpec]

默认管道包含四个阶段，每个阶段用不同的 system_prompt 创建专门的 ReActAgent。

**Orchestrator** 是执行引擎：

.. code-block:: python

    class AutoHarnessOrchestrator:
        async def run(self, task):
            context = task
            for stage in self._pipeline.stages:
                agent = self._create_agent_for_stage(stage)
                result = await agent.run({"query": context})
                # 上一个阶段的结果作为下一个阶段的输入
                context = f"Previous: {result}\n\nOriginal: {task}"
            return results

关键设计：每个阶段的输出成为下一阶段的输入。这样信息在管道中流动，
后面的 agent 可以基于前面的分析做决策。

**ExperienceStore** 跨运行学习：

.. code-block:: python

    class ExperienceStore:
        def record(self, stage, task, result):
            # 记录每次管道运行中每个阶段的输入输出
            ...

        def recent(self, stage=None, limit=10):
            # 查询历史记录，用于改进未来的运行
            ...

为什么这样设计？
----------------

1. **专业化**：每个阶段只做一件事。assess 不需要会写代码，verify 不需要会分析。分开的 agent 比一个"万能 agent"更精准。

2. **可组合**：管道可以自定义。加一个 lint 阶段、去一个 verify 阶段、或者换成完全不同的顺序。

3. **可追溯**：每个阶段的输入输出都被记录。出问题时可以定位是哪个阶段出了错。

4. **可学习**：ExperienceStore 积累历史，未来可以用这些数据自动改进管道本身（这就是 auto_harness 的"auto"部分）。

与其它模块的关系
-----------------

.. code-block:: text

    auto_harness/
    ├── pipeline.py       ← 定义管道结构 (StageSpec, PipelineSpec)
    ├── orchestrator.py   ← 执行管道 (AutoHarnessOrchestrator)
    └── experience.py     ← 经验积累 (ExperienceStore)

    依赖:
    ├── core/foundation/  ← OpenAIClient (LLM 调用)
    ├── core/single_agent ← ReActAgent (每个阶段的执行者)
    └── harness/          ← DeepAgent (被优化的对象)

使用示例
--------

.. code-block:: python

    client = OpenAIClient.from_env()
    orchestrator = AutoHarnessOrchestrator(client)

    result = await orchestrator.run("Improve error handling in auth.py")

    for stage, output in result["results"].items():
        print(f"[{stage}] {output['result'][:100]}")

    print(f"Total experiences: {len(orchestrator.experience)}")
