"""
Techs module - Technology management for Genie Engine.

Provides:
- TechManager: Create, copy, get, delete technologies
- TechHandle: Wrapper with attribute access
"""
from Actual_Tools.Techs.tech_manager import TechManager
from Actual_Tools.Techs.tech_handle import TechHandle

__all__ = ["TechManager", "TechHandle"]
