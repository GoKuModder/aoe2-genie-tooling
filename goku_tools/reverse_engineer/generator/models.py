"""
Models for RECodeGenerator.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

@dataclass
class UnitGroup:
    """A group of connected units, graphics, and sounds."""
    name: str
    unit_ids: Set[int] = field(default_factory=set)
    graphic_ids: Set[int] = field(default_factory=set)
    sound_ids: Set[int] = field(default_factory=set)
    
    # Track which links exist within this group
    internal_links: Dict[str, List[Tuple[int, str, int]]] = field(default_factory=dict)
    # Links to objects in OTHER groups
    external_links: Dict[str, List[Tuple[int, str, int]]] = field(default_factory=dict)
    
    @property
    def folder_name(self) -> str:
        """Generate safe folder name."""
        safe = re.sub(r'[^\w\s-]', '', self.name.lower())
        safe = re.sub(r'[\s]+', '_', safe)
        return f"group_{safe}"


@dataclass
class IndependentObjects:
    """Standalone objects that have no connections to other above-threshold objects."""
    unit_ids: Set[int] = field(default_factory=set)
    graphic_ids: Set[int] = field(default_factory=set)
    sound_ids: Set[int] = field(default_factory=set)


@dataclass
class LinkSpec:
    """
    Description of a link that should be applied after object creation.

    Attributes:
        field: Attribute path on the object (e.g., "standing_sprite_id1", "tasks[0].proceeding_graphic_id").
        target_id: ID value read from the DAT file.
        target_type: One of "unit", "graphic", or "sound".
    """
    field: str
    target_id: int
    target_type: str
