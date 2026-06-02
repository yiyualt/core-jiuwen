# coding: utf-8
"""Agent Teams — multi-agent collaboration system.

CoordinatorAgent delegates tasks to specialized member agents,
enabling complex multi-step workflows. Includes message passing,
task schemas, and agent spawning.
"""

from jiuwen.core.agent_teams.team import Team, CoordinatorAgent
from jiuwen.core.agent_teams.messager import InProcessMessager
from jiuwen.core.agent_teams.schema import TeamEvent, TaskBlueprint
from jiuwen.core.agent_teams.spawn import AgentSpawner

__all__ = ["Team", "CoordinatorAgent", "InProcessMessager", "TeamEvent", "TaskBlueprint", "AgentSpawner"]
