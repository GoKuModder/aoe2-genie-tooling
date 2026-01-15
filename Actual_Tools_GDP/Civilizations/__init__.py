"""
Civilizations module - Civilization management for Genie Engine.

Provides:
- CivManager: Get, copy, manage civilizations and global resources
- CivHandle: Wrapper for individual civilizations
- ResourceAccessor: Per-civ resource value access
"""
from .civ_manager import CivManager
from .civ_handle import CivHandle
from .resource_accessor import ResourceAccessor

__all__ = ["CivManager", "CivHandle", "ResourceAccessor"]
