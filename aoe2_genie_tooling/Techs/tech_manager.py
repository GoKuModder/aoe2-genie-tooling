"""
TechManager - Manages tech/technology operations.

Techs are single-tier objects (unlike Sounds/Effects which have nested lists).
Each Tech has properties like name, effect_id, costs, etc.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace
    from aoe2_genie_tooling.Techs.tech_handle import TechHandle

from aoe2_genie_tooling.Techs.tech_handle import TechHandle

__all__ = ["TechManager"]


class TechManager:
    """
    Manager for tech operations.
    
    Techs define research items linked to Effects.
    """
    
    def __init__(self, workspace: GenieWorkspace) -> None:
        """Initialize TechManager with workspace reference."""
        self.workspace = workspace
    
    def get(self, tech_id: int) -> TechHandle:
        """
        Get a tech by ID.
        
        Args:
            tech_id: ID of the tech
            
        Returns:
            TechHandle for the tech
            
        Raises:
            InvalidIdError: If tech_id is out of range
        """
        from aoe2_genie_tooling.Base.core.exceptions import InvalidIdError
        
        if tech_id < 0 or tech_id >= len(self.workspace.dat.techs):
            raise InvalidIdError(
                f"Tech ID {tech_id} out of range (0-{len(self.workspace.dat.techs)-1})"
            )
        
        return TechHandle(self.workspace, tech_id)
    
    def count(self) -> int:
        """Get total number of tech slots."""
        return len(self.workspace.dat.techs)

    def exists(self, tech_id: int) -> bool:
        """Check if tech exists and is not None."""
        if 0 <= tech_id < len(self.workspace.dat.techs):
            return self.workspace.dat.techs[tech_id] is not None
        return False
        
    def count_active(self) -> int:
        """Get number of non-None techs."""
        return sum(1 for t in self.workspace.dat.techs if t is not None)

    def _create_blank_tech(self, ver: Any) -> Any:
        """Create a blank Tech object."""
        from sections.tech.tech import Tech
        t = Tech(ver=ver)
        try:
            t.name = ""
        except Exception:
            pass
        t.effect_id = -1
        return t

    def delete(self, tech_id: int) -> bool:
        """
        Reset a tech to blank values.
        
        Args:
            tech_id: ID to reset
            
        Returns:
            True if reset, False if out of range
        """
        if self.exists(tech_id):
            template = self.workspace.dat.techs[tech_id]
            self.workspace.dat.techs[tech_id] = self._create_blank_tech(template.ver)
            return True
        return False

    def find_by_name(self, name: str) -> Optional[TechHandle]:
        """Find first tech matching name."""
        for i, tech in enumerate(self.workspace.dat.techs):
            if tech is not None:
                tech_name = ""
                try:
                    tech_name = tech.name
                except Exception:
                    pass
                if tech_name == name:
                    return TechHandle(self.workspace, i)
        return None

    def add_new(
        self,
        name: str = "",
        effect_id: int = -1,
        tech_id: Optional[int] = None,
    ) -> TechHandle:
        """
        Add a new tech to the DAT file.
        
        Args:
            name: Tech name
            effect_id: Effect ID to link (default: -1 = none)
            tech_id: Target ID. If None, appends to end
            
        Returns:
            TechHandle for the new tech
        """
        from sections.tech.tech import Tech
        
        target_idx = tech_id
        if target_idx is None:
            target_idx = len(self.workspace.dat.techs)
        
        # Find template for version
        template_ver = None
        for t in self.workspace.dat.techs:
            if t is not None:
                template_ver = t.ver
                break
        
        if template_ver is None:
            raise RuntimeError("Cannot add tech: DAT file has no existing techs")
             
        new_tech = Tech(ver=template_ver)
        try:
            new_tech.name = name
        except Exception:
            pass
        new_tech.effect_id = effect_id
        
        # Ensure capacity by filling with blank techs
        while len(self.workspace.dat.techs) <= target_idx:
            self.workspace.dat.techs.append(self._create_blank_tech(template_ver))
            
        self.workspace.dat.techs[target_idx] = new_tech
        return TechHandle(self.workspace, target_idx)

    # Alias
    create = add_new

    def copy(self, source_id: int, target_id: Optional[int] = None) -> TechHandle:
        """
        Copy a tech to a new ID.
        
        Args:
            source_id: Tech to copy
            target_id: Destination ID. If None, appends to end
            
        Returns:
            TechHandle for the copy
        """
        from aoe2_genie_tooling.Base.core.exceptions import InvalidIdError
        if not self.exists(source_id):
            raise InvalidIdError(f"Source tech {source_id} does not exist")
            
        source = self.workspace.dat.techs[source_id]
        new_obj = self._copy_tech(source)
        
        if target_id is None:
            target_id = len(self.workspace.dat.techs)
        
        while len(self.workspace.dat.techs) <= target_id:
            self.workspace.dat.techs.append(self._create_blank_tech(source.ver))
            
        self.workspace.dat.techs[target_id] = new_obj
        return TechHandle(self.workspace, target_id)

    def _copy_tech(self, source: Any) -> Any:
        """Manual copy of Tech object."""
        from sections.tech.tech import Tech
        new_tech = Tech(ver=source.ver)
        
        # Copy simple attrs
        simple_attrs = [
            'name', 'min_required_techs', 'civilization_id', 'full_tech_tree_mode',
            'location_unit_id', 'research_time', 'effect_id', 'type', 'icon_id',
            'button_id', 'help_str_id', 'tech_tree_str_id', 'hotkey_str_id',
            'name_str_id', 'description_str_id', 'repeatable'
        ]
        for attr in simple_attrs:
            try:
                setattr(new_tech, attr, getattr(source, attr))
            except Exception:
                pass
        
        # Copy lists
        try:
            new_tech.required_tech_ids = list(source.required_tech_ids)
        except Exception:
            pass
            
        # Copy costs
        try:
            new_tech.costs = [self._copy_cost(c) for c in source.costs]
        except Exception:
            pass
            
        return new_tech

    def _copy_cost(self, source: Any) -> Any:
        """Manual copy of TechCost object."""
        from sections.tech.tech_cost import TechCost
        new_cost = TechCost(ver=source.ver)
        attrs = ['resource_id', 'quantity', 'deduct_flag']
        for attr in attrs:
            try:
                setattr(new_cost, attr, getattr(source, attr))
            except Exception:
                pass
        return new_cost

    # Clipboard Implementation
    _clipboard: Optional[Any] = None

    def copy_to_clipboard(self, tech_id: int) -> bool:
        """Copy tech to internal clipboard."""
        if self.exists(tech_id):
            self.__class__._clipboard = self._copy_tech(self.workspace.dat.techs[tech_id])
            return True
        return False

    def paste(self, target_id: Optional[int] = None) -> Optional[TechHandle]:
        """Paste tech from clipboard."""
        if self.__class__._clipboard is None:
            return None
            
        pasted = self._copy_tech(self.__class__._clipboard)
        if target_id is None:
            target_id = len(self.workspace.dat.techs)
        
        while len(self.workspace.dat.techs) <= target_id:
            self.workspace.dat.techs.append(self._create_blank_tech(pasted.ver))
            
        self.workspace.dat.techs[target_id] = pasted
        return TechHandle(self.workspace, target_id)

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        self.__class__._clipboard = None
