"""Type stubs for CivManager - enables IDE autocomplete"""
from typing import Optional, Any
from aoe2_genie_tooling.Civilizations.civ_handle import CivHandle

class CivManager:
    """Manager for civilization operations."""
    
    def get(self, civ_id: int) -> CivHandle:
        """Get a civilization by ID."""
        ...
    
    def count(self) -> int:
        """Get total number of civilizations."""
        ...
    
    def exists(self, civ_id: int) -> bool:
        """Check if civilization exists."""
        ...

    def find_by_name(self, name: str) -> Optional[CivHandle]:
        """Find first civilization matching name."""
        ...

    def add_new(
        self,
        name: str = "",
        civ_id: Optional[int] = None,
    ) -> CivHandle:
        """Add a new civilization."""
        ...

    def create(
        self,
        name: str = "",
        civ_id: Optional[int] = None,
    ) -> CivHandle:
        """Alias for add_new."""
        ...

    def copy(self, source_id: int, target_id: Optional[int] = None) -> CivHandle:
        """Copy a civilization to a new ID."""
        ...

    def copy_to_clipboard(self, civ_id: int) -> bool:
        """Copy civilization to internal clipboard."""
        ...

    def paste(self, target_id: Optional[int] = None) -> Optional[CivHandle]:
        """Paste civilization from clipboard."""
        ...

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        ...

    # Global Resource Management
    def add_resource(self, default_value: float = 0.0) -> int:
        """
        Add a new resource to ALL civilizations.
        
        Resources are global - this adds a slot to every civilization.
        """
        ...

    def remove_resource(self, index: int) -> bool:
        """
        Remove a resource from ALL civilizations.
        
        Resources are global - this removes from every civilization.
        """
        ...

    def resource_count(self) -> int:
        """Get the number of resources (same across all civs)."""
        ...

    def clear_resources(self) -> None:
        """Remove all resources from ALL civilizations."""
        ...
