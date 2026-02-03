"""
EffectManager - Manager for effect (TechEffect) operations.

Effects follow a two-tier structure:
1. Effect Holder: A slot in the mega-list with a name
2. Effect Commands: The actual effect data inside each holder
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Union

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace
    from aoe2_genie_tooling.Effects.effect_handle import EffectHandle

from aoe2_genie_tooling.Effects.effect_handle import EffectHandle

__all__ = ["EffectManager"]


class EffectManager:
    """
    Manager for effect operations.
    
    Effects contain EffectCommands that define what happens
    when a technology is researched.
    """
    
    def __init__(self, workspace: GenieWorkspace) -> None:
        """Initialize EffectManager with workspace reference."""
        self.workspace = workspace
    
    def get(self, effect_id: int) -> EffectHandle:
        """
        Get an effect by ID.
        
        Args:
            effect_id: ID of the effect
            
        Returns:
            EffectHandle for the effect
            
        Raises:
            InvalidIdError: If effect_id is out of range
        """
        from aoe2_genie_tooling.Base.core.exceptions import InvalidIdError
        
        if effect_id < 0 or effect_id >= len(self.workspace.dat.tech_effects):
            raise InvalidIdError(
                f"Effect ID {effect_id} out of range (0-{len(self.workspace.dat.tech_effects)-1})"
            )
        
        return EffectHandle(self.workspace, effect_id)
    
    def count(self) -> int:
        """Get total number of effect slots."""
        return len(self.workspace.dat.tech_effects)

    def exists(self, effect_id: int) -> bool:
        """Check if effect exists and is not None."""
        if 0 <= effect_id < len(self.workspace.dat.tech_effects):
            return self.workspace.dat.tech_effects[effect_id] is not None
        return False
        
    def count_active(self) -> int:
        """Get number of non-None effects."""
        return sum(1 for e in self.workspace.dat.tech_effects if e is not None)

    def delete(self, effect_id: int) -> bool:
        """
        Reset an effect to blank values.
        
        Args:
            effect_id: ID to reset
            
        Returns:
            True if reset, False if out of range
        """
        if self.exists(effect_id):
            template = self.workspace.dat.tech_effects[effect_id]
            self.workspace.dat.tech_effects[effect_id] = self._create_blank_effect(template.ver)
            return True
        return False

    def find_by_name(self, name: str) -> Optional[EffectHandle]:
        """Find first effect matching name."""
        for i, effect in enumerate(self.workspace.dat.tech_effects):
            if effect is not None:
                effect_name = ""
                try:
                    effect_name = effect.name
                except Exception:
                    pass
                if effect_name == name:
                    return EffectHandle(self.workspace, i)
        return None

    def _create_blank_effect(self, ver: Any) -> Any:
        """Create a blank TechEffect object."""
        from sections.tech_effect.tech_effect import TechEffect
        e = TechEffect(ver=ver)
        try:
            e.name = ""
        except Exception:
            pass
        e.effects = []
        return e

    def add_new(
        self,
        name: str = "",
        effect_id: Optional[int] = None,
    ) -> EffectHandle:
        """
        Add a new effect holder to the DAT file.
        
        Args:
            name: Effect name
            effect_id: Target ID. If None, appends to end
            
        Returns:
            EffectHandle for the new effect holder
        """
        from sections.tech_effect.tech_effect import TechEffect
        
        target_idx = effect_id
        if target_idx is None:
            target_idx = len(self.workspace.dat.tech_effects)
        
        # Find template for version
        template_ver = None
        for e in self.workspace.dat.tech_effects:
            if e is not None:
                template_ver = e.ver
                break
        
        if template_ver is None:
            raise RuntimeError("Cannot add effect: DAT file has no existing effects")
             
        new_effect = TechEffect(ver=template_ver)
        try:
            new_effect.name = name
        except Exception:
            pass
        new_effect.effects = []
        
        # Ensure capacity by filling with blank effects
        while len(self.workspace.dat.tech_effects) <= target_idx:
            self.workspace.dat.tech_effects.append(self._create_blank_effect(template_ver))
            
        self.workspace.dat.tech_effects[target_idx] = new_effect
        return EffectHandle(self.workspace, target_idx)

    # Alias
    create = add_new

    def copy(self, source_id: int, target_id: Optional[int] = None) -> EffectHandle:
        """
        Copy an effect to a new ID.
        
        Args:
            source_id: Effect to copy
            target_id: Destination ID. If None, appends to end
            
        Returns:
            EffectHandle for the copy
        """
        from aoe2_genie_tooling.Base.core.exceptions import InvalidIdError
        if not self.exists(source_id):
            raise InvalidIdError(f"Source effect {source_id} does not exist")
            
        source = self.workspace.dat.tech_effects[source_id]
        new_obj = self._copy_effect(source)
        
        if target_id is None:
            target_id = len(self.workspace.dat.tech_effects)
        
        while len(self.workspace.dat.tech_effects) <= target_id:
            self.workspace.dat.tech_effects.append(self._create_blank_effect(source.ver))
            
        self.workspace.dat.tech_effects[target_id] = new_obj
        return EffectHandle(self.workspace, target_id)

    def _copy_effect(self, source: Any) -> Any:
        """Manual copy of TechEffect object."""
        from sections.tech_effect.tech_effect import TechEffect
        new_effect = TechEffect(ver=source.ver)
        try:
            new_effect.name = source.name
        except Exception:
            pass
        new_effect.effects = [self._copy_command(cmd) for cmd in source.effects]
        return new_effect

    def _copy_command(self, source: Any) -> Any:
        """Manual copy of EffectCommand object."""
        from sections.tech_effect.effect_command import EffectCommand
        new_cmd = EffectCommand(ver=source.ver)
        attrs = ['type', 'a', 'b', 'c', 'd']
        for attr in attrs:
            try:
                setattr(new_cmd, attr, getattr(source, attr))
            except Exception:
                pass
        return new_cmd

    # Clipboard Implementation
    _clipboard: Optional[Any] = None

    def copy_to_clipboard(self, effect_id: int) -> bool:
        """Copy effect to internal clipboard."""
        if self.exists(effect_id):
            self.__class__._clipboard = self._copy_effect(self.workspace.dat.tech_effects[effect_id])
            return True
        return False

    def paste(self, target_id: Optional[int] = None) -> Optional[EffectHandle]:
        """Paste effect from clipboard."""
        if self.__class__._clipboard is None:
            return None
            
        pasted = self._copy_effect(self.__class__._clipboard)
        if target_id is None:
            target_id = len(self.workspace.dat.tech_effects)
        
        while len(self.workspace.dat.tech_effects) <= target_id:
            self.workspace.dat.tech_effects.append(self._create_blank_effect(pasted.ver))
            
        self.workspace.dat.tech_effects[target_id] = pasted
        return EffectHandle(self.workspace, target_id)

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        self.__class__._clipboard = None
