"""
Effects module - Effect management for Genie Engine.

Provides:
- EffectManager: Create, clone, get, delete effects
- EffectHandle: Wrapper with command management
- EffectCommandHandle: Wrapper for individual commands
"""
from Actual_Tools.Effects.effect_manager import EffectManager
from Actual_Tools.Effects.effect_handle import EffectHandle, EffectCommandHandle

__all__ = ["EffectManager", "EffectHandle", "EffectCommandHandle"]
