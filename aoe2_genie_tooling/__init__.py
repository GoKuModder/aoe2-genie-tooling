"""
aoe2_genie_tooling - Production-quality tools layer for editing AoE2 DAT files.

This package provides an AoE2ScenarioParser-style API with GUI-like tabs
and intuitive managers for editing Genie Engine DAT files. It wraps
GenieDatParser (Rust-backed) with a user-friendly, Pythonic interface.

Quick Start:
    from aoe2_genie_tooling import GenieWorkspace

    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    
    # Access managers through workspace
    unit = workspace.unit_manager.get(4)
    tech = workspace.tech_manager.get(22)
    effect = workspace.effect_manager.get(100)
    
    # Use fluent API for effect commands
    effect.add_command.attribute_modifier_multiply(a=4, b=-1, c=9, d=1.15)
    
    workspace.save("output.dat")

Public API:
    - GenieWorkspace: Root entry point for DAT file editing
    - Managers: UnitManager, TechManager, EffectManager, GraphicManager, SoundManager, CivManager
    - Handles: UnitHandle, TechHandle, EffectHandle, GraphicHandle, SoundHandle, CivHandle
    - logger: Colored console output (can be disabled with logger.disable())
    - registry: JSON export for created items
"""

from aoe2_genie_tooling.Base.workspace import GenieWorkspace
from aoe2_genie_tooling.Base.core.logger import Logger
from aoe2_genie_tooling.Base.core.registry import Registry
from aoe2_genie_tooling.Base.core.exceptions import (
    GenieToolsError,
    GapNotAllowedError,
    InvalidIdError,
    TemplateNotFoundError,
    UnitIdConflictError,
    ValidationError,
)

# Managers
from aoe2_genie_tooling.Units.unit_manager import UnitManager
from aoe2_genie_tooling.Techs.tech_manager import TechManager
from aoe2_genie_tooling.Effects.effect_manager import EffectManager
from aoe2_genie_tooling.Graphics.graphic_manager import GraphicManager
from aoe2_genie_tooling.Sounds.sound_manager import SoundManager
from aoe2_genie_tooling.Civilizations.civ_manager import CivManager

# Handles
from aoe2_genie_tooling.Units.unit_handle import UnitHandle
from aoe2_genie_tooling.Units.task_builder import TaskBuilder
from aoe2_genie_tooling.Techs.tech_handle import TechHandle
from aoe2_genie_tooling.Effects.effect_handle import EffectHandle
from aoe2_genie_tooling.Effects.command_handle import CommandHandle
from aoe2_genie_tooling.Effects.effect_command_builder import EffectCommandBuilder
from aoe2_genie_tooling.Graphics.graphic_handle import GraphicHandle
from aoe2_genie_tooling.Sounds.sound_handle import SoundHandle
from aoe2_genie_tooling.Civilizations.civ_handle import CivHandle

# Create singleton instances for backward compatibility
logger = Logger()
registry = Registry()

__all__ = [
    # Core
    "GenieWorkspace",
    # Managers
    "UnitManager",
    "TechManager",
    "EffectManager",
    "GraphicManager",
    "SoundManager",
    "CivManager",
    # Handles
    "UnitHandle",
    "TaskBuilder",
    "TechHandle",
    "EffectHandle",
    "CommandHandle",
    "EffectCommandBuilder",
    "GraphicHandle",
    "SoundHandle",
    "CivHandle",
    # Logging/Registry
    "logger",
    "registry",
    # Exceptions
    "GenieToolsError",
    "GapNotAllowedError",
    "InvalidIdError",
    "TemplateNotFoundError",
    "UnitIdConflictError",
    "ValidationError",
]

__version__ = "1.3.0"

