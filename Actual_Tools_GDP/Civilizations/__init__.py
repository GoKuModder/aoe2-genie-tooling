"""
Civilizations module - Civilization management for Genie Engine.

Provides:
- CivilizationsManager: Query and access civilizations
- CivHandle: Wrapper with attribute access
"""
from .civ_manager import CivilizationsManager
from .civ_handle import CivHandle

__all__ = ["CivilizationsManager", "CivHandle"]
