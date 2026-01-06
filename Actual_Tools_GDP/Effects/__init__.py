"""
Effects module - Effect management for Genie Engine.

Provides:
- EffectManager: Create, copy, get, delete effect holders
- EffectHandle: Wrapper for effect holder with command management
- CommandHandle: Wrapper for individual effect commands
"""
from .effect_manager import EffectManager
from .effect_handle import EffectHandle
from .command_handle import CommandHandle

__all__ = ["EffectManager", "EffectHandle", "CommandHandle"]
