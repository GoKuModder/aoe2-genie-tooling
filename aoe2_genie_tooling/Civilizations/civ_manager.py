"""
CivManager - Manager for civilization operations.

Civilizations contain units, resources, and effect links.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace
    from aoe2_genie_tooling.Civilizations.civ_handle import CivHandle

from aoe2_genie_tooling.Civilizations.civ_handle import CivHandle

__all__ = ["CivManager"]


class CivManager:
    """
    Manager for civilization operations.
    """
    
    def __init__(self, workspace: GenieWorkspace) -> None:
        """Initialize CivManager with workspace reference."""
        self.workspace = workspace
    
    def get(self, civ_id: int) -> CivHandle:
        """
        Get a civilization by ID.
        
        Args:
            civ_id: ID of the civilization
            
        Returns:
            CivHandle for the civilization
            
        Raises:
            InvalidIdError: If civ_id is out of range
        """
        from aoe2_genie_tooling.Base.core.exceptions import InvalidIdError
        
        if civ_id < 0 or civ_id >= len(self.workspace.dat.civilizations):
            raise InvalidIdError(
                f"Civ ID {civ_id} out of range (0-{len(self.workspace.dat.civilizations)-1})"
            )
        
        return CivHandle(self.workspace, civ_id)
    
    def count(self) -> int:
        """Get total number of civilizations."""
        return len(self.workspace.dat.civilizations)

    def exists(self, civ_id: int) -> bool:
        """Check if civilization exists."""
        return 0 <= civ_id < len(self.workspace.dat.civilizations)

    def find_by_name(self, name: str) -> Optional[CivHandle]:
        """Find first civilization matching name."""
        for i, civ in enumerate(self.workspace.dat.civilizations):
            if civ is not None:
                civ_name = ""
                try:
                    civ_name = civ.name
                except Exception:
                    pass
                if civ_name == name:
                    return CivHandle(self.workspace, i)
        return None

    def _create_blank_civ(self, ver: Any) -> Any:
        """Create a blank Civilization object."""
        from sections.civilization.civilization import Civilization
        c = Civilization(ver=ver)
        try:
            c.name = ""
        except Exception:
            pass
        c.resources = []
        c.units = []
        return c

    def add_new(
        self,
        name: str = "",
        civ_id: Optional[int] = None,
    ) -> CivHandle:
        """
        Add a new civilization to the DAT file.
        
        Args:
            name: Civilization name
            civ_id: Target ID. If None, appends to end
            
        Returns:
            CivHandle for the new civilization
        """
        from sections.civilization.civilization import Civilization
        
        target_idx = civ_id
        if target_idx is None:
            target_idx = len(self.workspace.dat.civilizations)
        
        # Find template for version
        template_ver = None
        for c in self.workspace.dat.civilizations:
            if c is not None:
                template_ver = c.ver
                break
        
        if template_ver is None:
            raise RuntimeError("Cannot add civilization: DAT file has no existing civilizations")
             
        new_civ = Civilization(ver=template_ver)
        try:
            new_civ.name = name
        except Exception:
            pass
        new_civ.resources = []
        new_civ.units = []
        
        # Ensure capacity
        while len(self.workspace.dat.civilizations) <= target_idx:
            self.workspace.dat.civilizations.append(self._create_blank_civ(template_ver))
            
        self.workspace.dat.civilizations[target_idx] = new_civ
        return CivHandle(self.workspace, target_idx)

    # Alias
    create = add_new

    def copy(self, source_id: int, target_id: Optional[int] = None) -> CivHandle:
        """
        Copy a civilization to a new ID.
        
        Args:
            source_id: Civilization to copy
            target_id: Destination ID. If None, appends to end
            
        Returns:
            CivHandle for the copy
        """
        from aoe2_genie_tooling.Base.core.exceptions import InvalidIdError
        if not self.exists(source_id):
            raise InvalidIdError(f"Source civilization {source_id} does not exist")
            
        source = self.workspace.dat.civilizations[source_id]
        new_obj = self._copy_civ(source)
        
        if target_id is None:
            target_id = len(self.workspace.dat.civilizations)
        
        while len(self.workspace.dat.civilizations) <= target_id:
            self.workspace.dat.civilizations.append(self._create_blank_civ(source.ver))
            
        self.workspace.dat.civilizations[target_id] = new_obj
        return CivHandle(self.workspace, target_id)

    def _copy_civ(self, source: Any) -> Any:
        """Manual copy of Civilization object."""
        from sections.civilization.civilization import Civilization
        new_civ = Civilization(ver=source.ver)
        
        # Copy simple attrs
        simple_attrs = [
            'name', 'player_type', 'num_resources', 'tech_tree_effect_id',
            'team_bonus_effect_id', 'icon_set'
        ]
        for attr in simple_attrs:
            try:
                setattr(new_civ, attr, getattr(source, attr))
            except Exception:
                pass
        
        # Copy resources list
        try:
            new_civ.resources = list(source.resources)
        except Exception:
            new_civ.resources = []
            
        # Copy units list (reference copy, not deep copy of units)
        try:
            new_civ.units = list(source.units)
        except Exception:
            new_civ.units = []
            
        return new_civ

    # Clipboard Implementation
    _clipboard: Optional[Any] = None

    def copy_to_clipboard(self, civ_id: int) -> bool:
        """Copy civilization to internal clipboard."""
        if self.exists(civ_id):
            self.__class__._clipboard = self._copy_civ(self.workspace.dat.civilizations[civ_id])
            return True
        return False

    def paste(self, target_id: Optional[int] = None) -> Optional[CivHandle]:
        """Paste civilization from clipboard."""
        if self.__class__._clipboard is None:
            return None
            
        pasted = self._copy_civ(self.__class__._clipboard)
        if target_id is None:
            target_id = len(self.workspace.dat.civilizations)
        
        while len(self.workspace.dat.civilizations) <= target_id:
            self.workspace.dat.civilizations.append(self._create_blank_civ(pasted.ver))
            
        self.workspace.dat.civilizations[target_id] = pasted
        return CivHandle(self.workspace, target_id)

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        self.__class__._clipboard = None

    # ==========================================================================
    # GLOBAL RESOURCE MANAGEMENT
    # Resources must be added/removed across ALL civilizations simultaneously
    # ==========================================================================

    def add_resource(self, default_value: float = 0.0) -> int:
        """
        Add a new resource to ALL civilizations.
        
        Resources are global - each civ must have the same number of resource slots.
        This adds a new slot to every civilization with the specified default value.
        
        Args:
            default_value: Initial value for the new resource in all civs
            
        Returns:
            Index of the new resource
        """
        new_index = -1
        for civ in self.workspace.dat.civilizations:
            if civ is not None:
                civ.resources.append(default_value)
                civ.num_resources = len(civ.resources)
                new_index = len(civ.resources) - 1
        return new_index

    def remove_resource(self, index: int) -> bool:
        """
        Remove a resource from ALL civilizations.
        
        Resources are global - each civ must have the same number of resource slots.
        This removes the resource at the specified index from every civilization.
        
        Args:
            index: Resource index to remove
            
        Returns:
            True if removed, False if index invalid
        """
        # Validate index on first civ
        first_civ = None
        for civ in self.workspace.dat.civilizations:
            if civ is not None:
                first_civ = civ
                break
        
        if first_civ is None or not (0 <= index < len(first_civ.resources)):
            return False
        
        # Remove from all civs
        for civ in self.workspace.dat.civilizations:
            if civ is not None:
                if 0 <= index < len(civ.resources):
                    del civ.resources[index]
                    civ.num_resources = len(civ.resources)
        return True

    def resource_count(self) -> int:
        """
        Get the number of resources (same across all civs).
        
        Returns:
            Number of resource slots
        """
        for civ in self.workspace.dat.civilizations:
            if civ is not None:
                return len(civ.resources)
        return 0

    def clear_resources(self) -> None:
        """Remove all resources from ALL civilizations."""
        for civ in self.workspace.dat.civilizations:
            if civ is not None:
                civ.resources = []
                civ.num_resources = 0
