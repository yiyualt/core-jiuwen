# coding: utf-8
"""LearningsStage — post-session reflection and experience extraction."""

from jiuwen.core.foundation.llm import LLMClient
from jiuwen.core.single_agent.agents import ReActAgent
from jiuwen.auto_harness.contexts import SessionContext
from jiuwen.auto_harness.experience import ExperienceStore
from jiuwen.auto_harness.stages import BaseStage, StageResult


class LearningsStage(BaseStage):
    """Reflects on the entire session and extracts learnings.

    After all tasks are complete, this stage reviews successes and
    failures, and records structured insights to the experience store.

    Usage::

        stage = LearningsStage(client, experience_store)
        result = await stage.execute(ctx)
    """

    name = "learnings"
    description = "Post-session reflection and learning extraction"

    def __init__(self, client: LLMClient, experience: ExperienceStore):
        self._client = client
        self._experience = experience

    async def execute(self, ctx: SessionContext) -> StageResult:
        # Collect session results
        session_summary_parts = []
        for key, value in ctx.artifacts.items():
            if hasattr(value, "output"):
                session_summary_parts.append(f"[{key}] {str(value.output)[:500]}")

        if not session_summary_parts:
            return StageResult(stage_name=self.name, status="success",
                              output="No session results to reflect on.")

        summary = "\n\n".join(session_summary_parts)

        # Load existing experiences for context
        existing = self._experience.recent(limit=20)
        existing_context = self._experience.synthesize(existing, max_tokens=1000)

        # Let the agent reflect
        agent = ReActAgent(
            client=self._client,
            system_prompt=(
                "You analyze optimization sessions and extract actionable learnings. "
                "For each learning, identify: type (SUCCESS/FAILURE/INSIGHT), "
                "a short topic, and a clear summary of what was learned."
            ),
        )

        query = (
            f"Session results:\n{summary}\n\n"
            f"Previous experiences:\n{existing_context}\n\n"
            f"Extract 2-5 key learnings from this session. "
            f"For each, specify type (SUCCESS/FAILURE/INSIGHT), topic, and summary."
        )

        result = await agent.run({"query": query})
        output = str(result.get("result", ""))

        # Parse and record learnings
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
            exp_type = ExperienceStore.INSIGHT
            if "SUCCESS" in line.upper():
                exp_type = ExperienceStore.SUCCESS
            elif "FAIL" in line.upper():
                exp_type = ExperienceStore.FAILURE

            if ":" in line:
                parts = line.split(":", 1)
                topic = parts[0].strip()[:100]
                detail = parts[1].strip() if len(parts) > 1 else ""
            else:
                topic = "session reflection"
                detail = line

            self._experience.record("learnings", topic, {"result": detail}, exp_type=exp_type)

        return StageResult(
            stage_name=self.name,
            status="success",
            output=output,
            messages=[f"Extracted learnings from session"],
        )
