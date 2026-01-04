"""
Graphics module - Graphic management for Genie Engine.

Provides:
- GraphicManager: Add, copy, delete, paste graphics
- GraphicHandle: High-level wrapper with full attribute access
"""
from Actual_Tools_GDP.Graphics.graphic_manager import GraphicManager
from Actual_Tools_GDP.Graphics.graphic_handle import GraphicHandle

__all__ = ["GraphicManager", "GraphicHandle"]
