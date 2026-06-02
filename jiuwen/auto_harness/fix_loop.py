# coding: utf-8
"""FixLoopController — CI-driven retry loop with error injection.

Concrete implementations:
- CommandVerifier: runs shell commands as verify_fn
- AgentFixer: invokes ReActAgent as fix_fn
- OutputEvaluator: assesses fix quality as evaluator
- FixLoopExecutor: composes all three with FixLoopController
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable

from jiuwen.auto_harness.contexts import SessionContext
from jiuwen.auto_harness.stages import BaseStage, StageResult


@dataclass
class FixLoopResult:
    """Outcome of a fix loop verification + fix cycle."""
    success: bool
    attempts: int = 0
    phase: int = 1
    error_log: list[str] = field(default_factory=list)
    output: str = ""


class FixLoopController:
    """Two-phase CI-driven retry controller.

    Phase 1: Agent fixes based on CI errors (up to p1_max retries)
    Phase 2: Evaluator reviews quality (up to p2_max retries)

    Usage::

        fix = FixLoopController(phase1_max_retries=5, phase2_max_retries=3)

        async def verify(): return FixLoopResult(success=..., error_log=[...])
        async def fix_errs(errors): await agent.run({"query": f"Fix: {errors}"})
        async def evaluate(output): return "pass" in output.lower()

        result = await fix.run(verify, fix_errs, evaluator=evaluate)
    """

    def __init__(self, phase1_max_retries: int = 5, phase2_max_retries: int = 3):
        self._p1_max = phase1_max_retries
        self._p2_max = phase2_max_retries

    async def run(
        self,
        verify_fn: Callable[[], Awaitable[FixLoopResult]],
        fix_fn: Callable[[list[str]], Awaitable[Any]] | None = None,
        evaluator: Callable[[str], Awaitable[bool]] | None = None,
    ) -> FixLoopResult:
        total = 0
        # Phase 1
        for _ in range(self._p1_max):
            result = await verify_fn()
            total += 1
            if result.success:
                return FixLoopResult(success=True, attempts=total, phase=1, output=result.output)
            if fix_fn:
                await fix_fn(result.error_log)
        # Phase 2
        if evaluator:
            for _ in range(self._p2_max):
                result = await verify_fn()
                total += 1
                if result.success:
                    return FixLoopResult(success=True, attempts=total, phase=2, output=result.output)
                if fix_fn:
                    combined = "\n".join(result.error_log)
                    if await evaluator(combined):
                        return FixLoopResult(success=True, attempts=total, phase=2, output=result.output)
                    await fix_fn([f"Evaluator rejected: {combined}"])
        return FixLoopResult(success=False, attempts=total, phase=2, error_log=["All fix attempts exhausted"])

    def should_retry(self, stage_name: str) -> bool:
        return True

    async def handle_failure(self, stage: BaseStage, ctx: SessionContext, result: StageResult) -> StageResult:
        return result  # actual fix logic in verify stage

    def reset(self) -> None:
        pass


class CommandVerifier:
    """Runs shell commands as a verification step.

    Executes a list of commands sequentially via subprocess. Returns
    FixLoopResult with success=True only if all commands exit 0.

    Usage::

        verifier = CommandVerifier(commands=["pytest -x", "ruff check ."])
        result = await verifier.verify()
        # result.success is True if all commands pass
    """

    def __init__(self, commands: list[str], timeout: int = 300):
        self._commands = commands
        self._timeout = timeout

    async def verify(self) -> FixLoopResult:
        """Execute all commands. Return FixLoopResult indicating success/failure."""
        errors = []
        for cmd in self._commands:
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd.split(),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                try:
                    stdout, stderr = await asyncio.wait_for(
                        proc.communicate(), timeout=self._timeout
                    )
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
                    errors.append(f"TIMEOUT ({self._timeout}s): {cmd}")
                    continue

                if proc.returncode != 0:
                    err_text = stderr.decode(errors="replace").strip()
                    if not err_text:
                        err_text = stdout.decode(errors="replace").strip()
                    errors.append(f"FAILED (exit {proc.returncode}): {cmd}\n{err_text}")
            except FileNotFoundError:
                errors.append(f"NOT FOUND: {cmd}")
            except Exception as exc:
                errors.append(f"ERROR: {cmd} — {exc}")

        if errors:
            return FixLoopResult(success=False, error_log=errors, output="\n".join(errors))
        return FixLoopResult(success=True, output="All commands passed")


class AgentFixer:
    """Invokes a ReActAgent to fix reported errors.

    Receives a list of error messages, concatenates them into a prompt,
    and delegates to the agent to modify source files.

    Usage::

        fixer = AgentFixer(client=llm_client)
        await fixer.fix(["FAILED test_login — AssertionError: expected 200 got 401"])
    """

    FIX_SYSTEM_PROMPT = (
        "You are an expert developer fixing code issues. "
        "You have access to the filesystem — read the relevant source files, "
        "understand the errors, locate the root cause, and apply fixes directly. "
        "For each fix:\n"
        "1. Read the file where the error occurs\n"
        "2. Identify the root cause (not just the symptom)\n"
        "3. Edit the file with the minimal necessary change\n"
        "4. Explain what you changed and why\n"
        "Be precise. Do not refactor unrelated code. Do not guess — read files first."
    )

    def __init__(self, client):
        self._client = client

    async def fix(self, errors: list[str]) -> None:
        """Run the agent to fix the given errors."""
        from jiuwen.core.single_agent.agents import ReActAgent

        combined = "\n\n".join(errors)
        agent = ReActAgent(
            client=self._client,
            system_prompt=self.FIX_SYSTEM_PROMPT,
        )
        await agent.run({
            "query": (
                f"The following errors were detected. Please fix them:\n\n"
                f"{combined}\n\n"
                f"Read the relevant files, identify root causes, and apply fixes."
            )
        })


class OutputEvaluator:
    """Assesses fix quality using configurable strategies.

    Strategies are tried in order until one returns a definitive boolean result.
    Supported strategies:
    - ("command", {"cmd": "pytest -x"}) — run command, exit 0 = True
    - ("pattern", {"pattern": "PASSED", "mode": "include"}) — regex match
    - ("pattern", {"pattern": "FAILED", "mode": "exclude"}) — regex non-match
    - ("agent", {"client": llm}) — LLM judges output quality (slow, use as fallback)

    Usage::

        evaluator = OutputEvaluator(strategies=[
            ("command", {"cmd": "pytest -x --tb=short"}),
            ("pattern", {"pattern": r"\\d+ passed", "mode": "include"}),
        ])
        is_good = await evaluator.evaluate(output_text)
    """

    def __init__(self, strategies: list[tuple[str, dict]] | None = None):
        self._strategies = strategies or []

    async def evaluate(self, output: str) -> bool:
        """Try each strategy in order. First definitive result wins. Defaults to True."""
        for strategy_name, params in self._strategies:
            result = await self._try_strategy(strategy_name, params, output)
            if result is not None:
                return result
        # No strategy matched — default to accepting
        return True

    async def _try_strategy(self, name: str, params: dict, output: str) -> bool | None:
        if name == "command":
            return await self._eval_command(params)
        elif name == "pattern":
            return self._eval_pattern(params, output)
        elif name == "agent":
            return await self._eval_agent(params, output)
        return None

    async def _eval_command(self, params: dict) -> bool:
        cmd = params.get("cmd", "")
        if not cmd:
            return None
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd.split(),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
            return proc.returncode == 0
        except Exception:
            return False

    @staticmethod
    def _eval_pattern(params: dict, output: str) -> bool | None:
        pattern = params.get("pattern", "")
        mode = params.get("mode", "include")
        if not pattern:
            return None
        matched = bool(re.search(pattern, output))
        if mode == "exclude":
            return not matched
        return matched

    async def _eval_agent(self, params: dict, output: str) -> bool | None:
        client = params.get("client")
        if not client:
            return None
        from jiuwen.core.single_agent.agents import ReActAgent

        agent = ReActAgent(
            client=client,
            system_prompt=(
                "You evaluate whether a code fix was successful. "
                "Reply with exactly PASS or FAIL based on the output provided."
            ),
        )
        result = await agent.run({
            "query": (
                f"Output after applying a fix:\n\n{output[:3000]}\n\n"
                f"Does this indicate the fix was successful? Reply PASS or FAIL."
            )
        })
        answer = str(result.get("result", "")).strip().upper()
        return "PASS" in answer


class FixLoopExecutor:
    """Composes CommandVerifier, AgentFixer, OutputEvaluator, and FixLoopController.

    Provides a one-stop entry point for running the verify-fix-evaluate loop.
    The ``from_config()`` factory creates a fully-wired instance from a dict.

    Usage::

        executor = FixLoopExecutor.from_config(client, {
            "verify_commands": ["pytest -x", "ruff check ."],
            "phase1_max_retries": 3,
            "phase2_max_retries": 2,
            "evaluate_strategies": [
                ("command", {"cmd": "pytest -x"}),
                ("pattern", {"pattern": "passed", "mode": "include"}),
            ],
        })
        result = await executor.run()
    """

    def __init__(
        self,
        verifier: CommandVerifier,
        fixer: AgentFixer,
        evaluator: OutputEvaluator,
        controller: FixLoopController,
    ):
        self._verifier = verifier
        self._fixer = fixer
        self._evaluator = evaluator
        self._controller = controller

    @classmethod
    def from_config(cls, client, config: dict) -> "FixLoopExecutor":
        """Build a FixLoopExecutor from a configuration dict.

        Supported keys:
        - verify_commands: list[str] (required)
        - phase1_max_retries: int (default 5)
        - phase2_max_retries: int (default 3)
        - evaluate_strategies: list[tuple] (optional)
        """
        commands = config.get("verify_commands", ["echo ok"])
        verifier = CommandVerifier(commands=commands)

        fixer = AgentFixer(client=client)

        strategies = config.get("evaluate_strategies", [
            ("pattern", {"pattern": r"(PASSED|passed|ok|success)", "mode": "include"}),
        ])
        evaluator = OutputEvaluator(strategies=strategies)

        controller = FixLoopController(
            phase1_max_retries=config.get("phase1_max_retries", 5),
            phase2_max_retries=config.get("phase2_max_retries", 3),
        )

        return cls(verifier, fixer, evaluator, controller)

    async def run(self) -> FixLoopResult:
        """Execute the full verify-fix-evaluate loop."""
        return await self._controller.run(
            verify_fn=self._verifier.verify,
            fix_fn=self._fixer.fix,
            evaluator=self._evaluator.evaluate,
        )
