# coding: utf-8
"""Rails system — composable agent middleware.

Rails intercept agent execution at before/after hooks,
enabling security checks, file sandboxing, logging, etc.
"""

from jiuwen.core.rails.base import BaseRail, RailPipeline
from jiuwen.core.rails.security_rail import SecurityRail

__all__ = ["BaseRail", "RailPipeline", "SecurityRail"]
