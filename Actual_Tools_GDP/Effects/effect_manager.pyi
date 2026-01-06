"""Type stubs for EffectManager - enables IDE autocomplete"""
from typing import Optional, Any
from Actual_Tools_GDP.Effects.effect_handle import EffectHandle

class EffectManager:
    """Manager for effect operations."""
    
    def get(self, effect_id: int) -> EffectHandle:
        """Get an effect by ID."""
        ...
    
    def count(self) -> int:
        """Get total number of effect slots."""
        ...
    
    def exists(self, effect_id: int) -> bool:
        """Check if effect exists and is not None."""
        ...
        
    def count_active(self) -> int:
        """Get number of non-None effects."""
        ...

    def delete(self, effect_id: int) -> bool:
        """Delete an effect (sets slot to None)."""
        ...

    def find_by_name(self, name: str) -> Optional[EffectHandle]:
        """Find first effect matching name."""
        ...

    def add_new(
        self,
        name: str = "",
        effect_id: Optional[int] = None,
    ) -> EffectHandle:
        """Add a new effect holder."""
        ...

    def create(
        self,
        name: str = "",
        effect_id: Optional[int] = None,
    ) -> EffectHandle:
        """Alias for add_new."""
        ...

    def copy(self, source_id: int, target_id: Optional[int] = None) -> EffectHandle:
        """Copy an effect to a new ID."""
        ...

    def copy_to_clipboard(self, effect_id: int) -> bool:
        """Copy effect to internal clipboard."""
        ...

    def paste(self, target_id: Optional[int] = None) -> Optional[EffectHandle]:
        """Paste effect from clipboard."""
        ...

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        ...
