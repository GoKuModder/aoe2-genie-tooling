"""Type stubs for TechManager - enables IDE autocomplete"""
from typing import Optional, Any
from aoe2_genie_tooling.Techs.tech_handle import TechHandle

class TechManager:
    """Manager for tech operations."""
    
    def get(self, tech_id: int) -> TechHandle:
        """Get a tech by ID."""
        ...
    
    def count(self) -> int:
        """Get total number of tech slots."""
        ...
    
    def exists(self, tech_id: int) -> bool:
        """Check if tech exists and is not None."""
        ...
        
    def count_active(self) -> int:
        """Get number of non-None techs."""
        ...

    def delete(self, tech_id: int) -> bool:
        """Reset a tech to blank values."""
        ...

    def find_by_name(self, name: str) -> Optional[TechHandle]:
        """Find first tech matching name."""
        ...

    def add_new(
        self,
        name: str = "",
        effect_id: int = -1,
        tech_id: Optional[int] = None,
    ) -> TechHandle:
        """Add a new tech."""
        ...

    def create(
        self,
        name: str = "",
        effect_id: int = -1,
        tech_id: Optional[int] = None,
    ) -> TechHandle:
        """Alias for add_new."""
        ...

    def copy(self, source_id: int, target_id: Optional[int] = None) -> TechHandle:
        """Copy a tech to a new ID."""
        ...

    def copy_to_clipboard(self, tech_id: int) -> bool:
        """Copy tech to internal clipboard."""
        ...

    def paste(self, target_id: Optional[int] = None) -> Optional[TechHandle]:
        """Paste tech from clipboard."""
        ...

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        ...
