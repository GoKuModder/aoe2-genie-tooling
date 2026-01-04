"""
TechManager - Manager for creating and modifying technologies.

This module provides the TechManager class for managing technologies
in the Genie Engine DAT file.
"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional

from genieutils.tech import Tech

from .tech_handle import TechHandle
from ..Shared.tool_base import ToolBase, tracks_creation
from Actual_Tools.exceptions import InvalidIdError, TemplateNotFoundError

if TYPE_CHECKING:
    from genieutils.datfile import DatFile

__all__ = ["TechManager"]


class TechManager(ToolBase):
    """
    Manager for creating and modifying technologies in a DAT file.
    
    Provides methods to add, copy, delete technologies and retrieve existing ones.
    
    Example:
        >>> tm = workspace.tech_manager()
        >>> tech = tm.create("Upgrade Archer", template_id=22)
        >>> tech.research_time = 30
    """

    def __init__(self, dat_file: DatFile) -> None:
        super().__init__(dat_file)

    # =========================================================================
    # CREATION
    # =========================================================================

    @tracks_creation("tech", name_param="name")
    def create(
        self,
        name: str,
        template_id: Optional[int] = None,
        tech_id: Optional[int] = None,
    ) -> TechHandle:
        """
        Create a new technology.
        
        Args:
            name: Name for the new technology.
            template_id: ID of tech to clone from. If None, uses first valid.
            tech_id: Target ID. If None, appends to end.
        
        Returns:
            TechHandle for the new tech.
        """
        if not name:
            raise ValueError("name cannot be empty.")
        
        template = self._find_template(template_id)
        new_tech = copy.deepcopy(template)
        
        if tech_id is None:
            tech_id = self.allocate_next_tech_id()
        else:
            self.validate_id_positive(tech_id, "tech_id")
        
        new_tech.id = tech_id
        new_tech.name = name
        
        self.ensure_capacity(self.dat_file.techs, tech_id)
        self.dat_file.techs[tech_id] = new_tech
        
        return TechHandle(tech_id, self.dat_file)
    
    # Keep old method for backwards compatibility
    def add_tech(
        self,
        name: str,
        template_id: Optional[int] = None,
        tech_id: Optional[int] = None,
    ) -> TechHandle:
        """Alias for create(). Deprecated."""
        return self.create(name, template_id, tech_id)
    
    def copy(
        self,
        source_id: int,
        name: Optional[str] = None,
        tech_id: Optional[int] = None,
    ) -> TechHandle:
        """
        Copy an existing tech.
        
        Args:
            source_id: ID of tech to copy.
            name: Name for the copy. If None, copies source name.
            tech_id: Target ID. If None, appends to end.
        
        Returns:
            TechHandle for the copied tech.
        """
        if not self.exists(source_id):
            raise TemplateNotFoundError(f"Tech {source_id} not found.")
        
        source = self.dat_file.techs[source_id]
        cloned = copy.deepcopy(source)
        
        if name is not None:
            cloned.name = name
        
        if tech_id is None:
            tech_id = self.allocate_next_tech_id()
        else:
            self.validate_id_positive(tech_id, "tech_id")
        
        cloned.id = tech_id
        
        self.ensure_capacity(self.dat_file.techs, tech_id)
        self.dat_file.techs[tech_id] = cloned
        
        return TechHandle(tech_id, self.dat_file)
    
    # =========================================================================
    # RETRIEVAL
    # =========================================================================
    
    def get(self, tech_id: int) -> TechHandle:
        """
        Get a TechHandle by ID.
        
        Args:
            tech_id: The tech ID.
        
        Returns:
            TechHandle (check .exists() if unsure).
        """
        return TechHandle(tech_id, self.dat_file)
    
    def get_raw(self, tech_id: int) -> Optional[Tech]:
        """Get raw Tech object by ID."""
        if 0 <= tech_id < len(self.dat_file.techs):
            return self.dat_file.techs[tech_id]
        return None

    def exists(self, tech_id: int) -> bool:
        """Check if a tech ID exists."""
        return (
            0 <= tech_id < len(self.dat_file.techs)
            and self.dat_file.techs[tech_id] is not None
        )

    def count(self) -> int:
        """Return total number of tech slots."""
        return len(self.dat_file.techs)
    
    def count_active(self) -> int:
        """Return number of non-None techs."""
        return sum(1 for t in self.dat_file.techs if t is not None)
    
    # =========================================================================
    # DELETION
    # =========================================================================
    
    def delete(self, tech_id: int) -> bool:
        """
        Delete a tech (set slot to None).
        
        Args:
            tech_id: ID of tech to delete.
        
        Returns:
            True if deleted, False if didn't exist.
        """
        if not self.exists(tech_id):
            return False
        
        self.dat_file.techs[tech_id] = None
        return True
    
    # =========================================================================
    # UTILITIES
    # =========================================================================
    
    def find_by_name(self, name: str) -> Optional[TechHandle]:
        """Find first tech matching name."""
        for i, tech in enumerate(self.dat_file.techs):
            if tech is not None and tech.name == name:
                return TechHandle(i, self.dat_file)
        return None
    
    def _find_template(self, template_id: Optional[int]) -> Tech:
        """Find a template tech to clone from."""
        if template_id is not None:
            if 0 <= template_id < len(self.dat_file.techs):
                tech = self.dat_file.techs[template_id]
                if tech is not None:
                    return tech
            raise TemplateNotFoundError(f"Tech template ID {template_id} not found.")
        
        for tech in self.dat_file.techs:
            if tech is not None:
                return tech
        
        raise TemplateNotFoundError("No valid tech found for template.")
