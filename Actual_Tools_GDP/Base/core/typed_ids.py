"""
Typed ID Wrappers for Semantic Type Safety.

These wrapper classes enable IDE type checking to catch when the wrong ID type
is passed to a parameter. They inherit from int so they work seamlessly with
existing code, but type checkers (mypy, Pylance) can distinguish them.

Usage:
    def add_delta(self, graphic_id: GraphicId, ...) -> DeltaHandle:
        ...
    
    # IDE will warn:
    add_delta(graphic_id=delta.delta_id)  # Type error: DeltaIndex != GraphicId

Add new ID types here as needed for other entity types.
"""
from __future__ import annotations

from typing import Union

__all__ = [
    # Base
    "TypedId",
    
    # Units
    "UnitId",
    "TaskIndex",
    "AttackIndex",
    "ArmorIndex",
    "DropSiteIndex",
    "TrainLocationIndex",
    "DamageGraphicIndex",
    
    # Graphics
    "GraphicId",
    "DeltaIndex",
    "AngleSoundIndex",
    
    # Sounds
    "SoundId",
    "SoundFileIndex",
    
    # Techs / Research
    "TechId",
    "ResearchLocationId",
    
    # Effects
    "EffectId",
    "EffectCommandIndex",
    
    # Civilizations
    "CivId",
    
    # Terrains
    "TerrainId",
    "TerrainTableIndex",
    
    # Resources
    "ResourceId",
    
    # Type aliases
    "GraphicIdLike",
    "UnitIdLike",
    "SoundIdLike",
]


class TypedId(int):
    """
    Base class for semantically-typed IDs.
    
    Inherits from int so these work anywhere an int is expected at runtime,
    but type checkers see them as distinct types.
    """
    
    def __new__(cls, value: int) -> "TypedId":
        return super().__new__(cls, value)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({int(self)})"


# =========================================================================
# UNITS
# =========================================================================

class UnitId(TypedId):
    """ID of a Unit in the DAT file."""
    pass


class TaskIndex(TypedId):
    """Index of a Task in a Unit's tasks list (0-based)."""
    pass


class AttackIndex(TypedId):
    """Index of an Attack in a Unit's attacks list (0-based)."""
    pass


class ArmorIndex(TypedId):
    """Index of an Armor entry in a Unit's armors list (0-based)."""
    pass


class DropSiteIndex(TypedId):
    """Index of a DropSite in a Unit's drop_sites list (0-based)."""
    pass


class TrainLocationIndex(TypedId):
    """Index of a TrainLocation in a Unit's train_locations list (0-based)."""
    pass


class DamageGraphicIndex(TypedId):
    """Index of a DamageGraphic in a Unit's damage_graphics list (0-based)."""
    pass


# =========================================================================
# GRAPHICS
# =========================================================================

class GraphicId(TypedId):
    """ID of a Graphic/Sprite in the DAT file."""
    pass


class DeltaIndex(TypedId):
    """Index of a Delta within a Graphic's deltas list (0-based)."""
    pass


class AngleSoundIndex(TypedId):
    """Index of an AngleSound in a Graphic's angle_sounds list (0-based)."""
    pass


# =========================================================================
# SOUNDS
# =========================================================================

class SoundId(TypedId):
    """ID of a Sound container in the DAT file."""
    pass


class SoundFileIndex(TypedId):
    """Index of a SoundFile within a Sound container's files list (0-based)."""
    pass


# =========================================================================
# TECHS / RESEARCH
# =========================================================================

class TechId(TypedId):
    """ID of a Technology in the DAT file."""
    pass


class ResearchLocationId(TypedId):
    """ID of a research location (building that can research)."""
    pass


# =========================================================================
# EFFECTS
# =========================================================================

class EffectId(TypedId):
    """ID of an Effect in the DAT file."""
    pass


class EffectCommandIndex(TypedId):
    """Index of a Command within an Effect's commands list (0-based)."""
    pass


# =========================================================================
# CIVILIZATIONS
# =========================================================================

class CivId(TypedId):
    """ID of a Civilization in the DAT file."""
    pass


# =========================================================================
# TERRAINS
# =========================================================================

class TerrainId(TypedId):
    """ID of a Terrain in the DAT file."""
    pass


class TerrainTableIndex(TypedId):
    """Index in a terrain table (0-based)."""
    pass


# =========================================================================
# RESOURCES
# =========================================================================

class ResourceId(TypedId):
    """ID of a Resource type (e.g., food=0, wood=1, stone=2, gold=3)."""
    pass


# =========================================================================
# TYPE ALIASES (for flexible parameter types)
# =========================================================================

# Parameters can accept either the typed ID or a raw int for convenience
GraphicIdLike = Union[GraphicId, int]
UnitIdLike = Union[UnitId, int]
SoundIdLike = Union[SoundId, int]
