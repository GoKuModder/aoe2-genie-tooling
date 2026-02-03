"""
IDTracker - Tracks ID uniqueness, moves, and reference updates.

Responsibilities:
- Validate IDs are unique before assignment
- Track ID movements (e.g., unit 400 → 399)
- Update references when IDs change
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Set

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace

__all__ = ["IDTracker"]


class IDTracker:
    """
    Tracks ID assignments and movements for reference integrity.
    
    Features:
    - Uniqueness validation: Ensures no duplicate IDs
    - Move tracking: Records ID changes for reference updates
    - Reference updating: Keeps cross-references valid after moves
    """
    
    def __init__(self) -> None:
        """Initialize tracker with empty state."""
        # Track which IDs are in use (type -> Set[id])
        self._used_ids: Dict[str, Set[int]] = {
            "units": set(),
            "graphics": set(),
            "sounds": set(),
            "techs": set(),
            "effects": set(),
        }
        
        # Track ID moves for reference updates (type -> {old_id: new_id})
        self._id_moves: Dict[str, Dict[int, int]] = {
            "units": {},
            "graphics": {},
            "sounds": {},
            "techs": {},
            "effects": {},
        }
    
    # -------------------------
    # ID Registration
    # -------------------------
    
    def register_id(self, obj_type: str, obj_id: int) -> None:
        """
        Register an ID as in-use.
        
        Args:
            obj_type: Type of object ("units", "graphics", etc.)
            obj_id: ID to register
        """
        if obj_type in self._used_ids:
            self._used_ids[obj_type].add(obj_id)
    
    def unregister_id(self, obj_type: str, obj_id: int) -> None:
        """
        Unregister an ID (after deletion).
        
        Args:
            obj_type: Type of object
            obj_id: ID to unregister
        """
        if obj_type in self._used_ids:
            self._used_ids[obj_type].discard(obj_id)
    
    def is_id_used(self, obj_type: str, obj_id: int) -> bool:
        """
        Check if an ID is already in use.
        
        Args:
            obj_type: Type of object
            obj_id: ID to check
            
        Returns:
            True if ID is in use
        """
        return obj_id in self._used_ids.get(obj_type, set())
    
    # -------------------------
    # ID Movement Tracking
    # -------------------------
    
    def track_move(self, obj_type: str, old_id: int, new_id: int) -> None:
        """
        Track that an object moved from old_id to new_id.
        
        Args:
            obj_type: Type of object
            old_id: Original ID
            new_id: New ID
        """
        if obj_type in self._id_moves:
            self._id_moves[obj_type][old_id] = new_id
            
            # Update used IDs
            self.unregister_id(obj_type, old_id)
            self.register_id(obj_type, new_id)
    
    def get_new_id(self, obj_type: str, old_id: int) -> Optional[int]:
        """
        Get the new ID for an object that moved.
        
        Args:
            obj_type: Type of object
            old_id: Original ID
            
        Returns:
            New ID if object moved, None otherwise
        """
        return self._id_moves.get(obj_type, {}).get(old_id)
    
    def clear_moves(self) -> None:
        """Clear all tracked moves (after save)."""
        for obj_type in self._id_moves:
            self._id_moves[obj_type].clear()
