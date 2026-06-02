# coding: utf-8
"""Handoff — transfer tasks between agents."""

from typing import Any


async def handoff(
    source_agent: Any,
    target_agent: Any,
    task: str,
    session: Any = None,
) -> dict[str, Any]:
    """Transfer a task from one agent to another.

    The source agent can hand off a task mid-execution. The target
    agent receives the task with context.

    Args:
        source_agent: The agent handing off the task.
        target_agent: The agent receiving the task.
        task: Task description.
        session: Optional session for context continuity.

    Returns:
        The target agent's result dict.
    """
    # Build context from source if available
    context_task = task
    if session:
        session.add_message("system", f"Task handed off: {task}")

    return await target_agent.run({"query": context_task}, session=session)
