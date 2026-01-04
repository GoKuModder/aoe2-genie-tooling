"""
Techs module - Technology management for Genie Engine.

Provides:
- TechManager: Create, copy, get, delete technologies
- TechHandle: Wrapper with attribute access
"""
from .tech_manager import TechManager
from .tech_handle import TechHandle

__all__ = ["TechManager", "TechHandle"]
