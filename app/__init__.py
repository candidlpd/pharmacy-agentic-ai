"""
Eli Lilly Enterprise Agentic AI Platform
Production Multi-Agent System
"""

__version__ = "1.0.0"
__author__ = "Eli Lilly AI Team"

from .config import settings
from .state import CaseState

__all__ = ["settings", "CaseState"]