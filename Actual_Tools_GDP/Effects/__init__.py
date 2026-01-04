"""
Effects module - Effect management for Genie Engine.

Provides:
- EffectManager: Create, clone, get, delete effects
- EffectHandle: Wrapper with command management
- EffectCommandHandle: Wrapper for individual commands
"""
from .effect_handle import EffectCommandHandle, EffectHandle
from .effect_manager import EffectManager

__all__ = ["EffectManager", "EffectHandle", "EffectCommandHandle"]
