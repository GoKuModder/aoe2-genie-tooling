"""
EffectManager - Manager for creating and modifying effects.

Effects in AoE2 contain EffectCommands that define what happens
when a technology is researched or a trigger fires.
"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, List, Optional

from genieutils.effect import Effect, EffectCommand

from Actual_Tools.Effects.effect_handle import EffectHandle
from Actual_Tools_GDP.Shared.tool_base import ToolBase, tracks_creation
from Actual_Tools.exceptions import InvalidIdError, TemplateNotFoundError

if TYPE_CHECKING:
    from genieutils.datfile import DatFile

__all__ = ["EffectManager"]


class EffectManager(ToolBase):
    """
    Manager for creating and modifying effects in a DAT file.
    
    Effects are collections of EffectCommands that modify game data.
    They are linked to Technologies via tech.effect_id.
    
    Example:
        >>> em = workspace.effect_manager()
        >>> effect = em.create("My Effect")
        >>> effect.add_command(type_=5, a=4, b=10)  # Set attack
    """
    
    def __init__(self, dat_file: DatFile) -> None:
        super().__init__(dat_file)
    
    # =========================================================================
    # CREATION
    # =========================================================================
    
    @tracks_creation("effect", name_param="name")
    def create(
        self,
        name: str = "",
        effect_id: Optional[int] = None,
    ) -> EffectHandle:
        """
        Create a new empty effect.
        
        Args:
            name: Name for the effect (optional).
            effect_id: Target ID. If None, appends to end.
        
        Returns:
            EffectHandle for the new effect.
        """
        if effect_id is None:
            effect_id = self.allocate_next_effect_id()
        else:
            self.validate_id_positive(effect_id, "effect_id")
        
        new_effect = Effect(
            name=name,
            effect_commands=[],
        )
        
        self.ensure_capacity(self.dat_file.effects, effect_id)
        self.dat_file.effects[effect_id] = new_effect
        
        return EffectHandle(effect_id, self.dat_file)
    
    def clone(
        self,
        source_id: int,
        name: Optional[str] = None,
        effect_id: Optional[int] = None,
    ) -> EffectHandle:
        """
        Clone an existing effect.
        
        Args:
            source_id: ID of effect to clone.
            name: Name for the clone. If None, copies from source.
            effect_id: Target ID. If None, appends to end.
        
        Returns:
            EffectHandle for the cloned effect.
        """
        if not self.exists(source_id):
            raise TemplateNotFoundError(f"Effect {source_id} not found.")
        
        source = self.dat_file.effects[source_id]
        cloned = copy.deepcopy(source)
        
        if name is not None:
            cloned.name = name
        
        if effect_id is None:
            effect_id = self.allocate_next_effect_id()
        else:
            self.validate_id_positive(effect_id, "effect_id")
        
        self.ensure_capacity(self.dat_file.effects, effect_id)
        self.dat_file.effects[effect_id] = cloned
        
        return EffectHandle(effect_id, self.dat_file)
    
    # =========================================================================
    # RETRIEVAL
    # =========================================================================
    
    def get(self, effect_id: int) -> EffectHandle:
        """
        Get an EffectHandle by ID.
        
        Args:
            effect_id: The effect ID.
        
        Returns:
            EffectHandle (check .exists() if unsure).
        """
        return EffectHandle(effect_id, self.dat_file)
    
    def get_raw(self, effect_id: int) -> Optional[Effect]:
        """
        Get raw Effect object by ID.
        
        Args:
            effect_id: The effect ID.
        
        Returns:
            Effect object or None.
        """
        if 0 <= effect_id < len(self.dat_file.effects):
            return self.dat_file.effects[effect_id]
        return None
    
    def exists(self, effect_id: int) -> bool:
        """Check if an effect ID exists."""
        return (
            0 <= effect_id < len(self.dat_file.effects)
            and self.dat_file.effects[effect_id] is not None
        )
    
    def count(self) -> int:
        """Return total number of effect slots."""
        return len(self.dat_file.effects)
    
    def count_active(self) -> int:
        """Return number of non-None effects."""
        return sum(1 for e in self.dat_file.effects if e is not None)
    
    # =========================================================================
    # DELETION
    # =========================================================================
    
    def delete(self, effect_id: int) -> bool:
        """
        Delete an effect (set slot to None).
        
        Args:
            effect_id: ID of effect to delete.
        
        Returns:
            True if deleted, False if didn't exist.
        """
        if not self.exists(effect_id):
            return False
        
        self.dat_file.effects[effect_id] = None
        return True
    
    # =========================================================================
    # UTILITIES
    # =========================================================================
    
    def find_by_name(self, name: str) -> Optional[EffectHandle]:
        """
        Find first effect matching name.
        
        Args:
            name: Name to search for.
        
        Returns:
            EffectHandle if found, None otherwise.
        """
        for i, effect in enumerate(self.dat_file.effects):
            if effect is not None and effect.name == name:
                return EffectHandle(i, self.dat_file)
        return None
    
    def allocate_next_effect_id(self) -> int:
        """Get the next available effect ID."""
        return len(self.dat_file.effects)
