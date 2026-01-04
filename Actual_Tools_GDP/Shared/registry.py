"""
Registry - JSON export for tracking created items with UUID-based identity.

Tracks units, graphics, sounds, techs, and effects created during a session.
Also supports dependency linking between objects.

Usage:
    from Actual_Tools_GDP.Shared.registry import registry
    
    # Items are auto-registered by managers
    workspace.units.create("My Unit", base_unit_id=4)
    
    # Export to JSON for ASP
    registry.save("genie_edits.json")
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

__all__ = ["registry", "Registry", "Dependency"]

PathLike = Union[str, Path]


@dataclass
class Dependency:
    """Represents a dependency between two objects."""
    source_type: str  # "unit", "tech", "effect", etc.
    source_id: int
    target_type: str
    target_id: int
    relation: str  # "uses_graphic", "uses_sound", "links_effect", etc.


@dataclass
class Registry:
    """
    Tracks created items for JSON export with UUID-based tracking.
    
    Features:
    - UUID-based persistent identity (survives ID changes)
    - Dependency tracking between objects
    - Effect registration
    - JSON export for AoE2ScenarioParser
    
    JSON Format:
    ```json
    {
        "units": [{"name": "Hero1", "id": 2800, "uuid": "abc-123"}],
        "effects": [{"name": "Upgrade Archer", "id": 100}],
        "dependencies": [{"source": "tech:50", "target": "effect:100"}]
    }
    ```
    """
    
    units: List[Dict[str, Any]] = field(default_factory=list)
    graphics: List[Dict[str, Any]] = field(default_factory=list)
    sounds: List[Dict[str, Any]] = field(default_factory=list)
    techs: List[Dict[str, Any]] = field(default_factory=list)
    effects: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[Dict[str, Any]] = field(default_factory=list)
    enabled: bool = True
    
    # UUID-to-ID mapping for persistent identity
    _uuid_map: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        "units": {}, "graphics": {}, "sounds": {}, "techs": {}, "effects": {}
    })
    
    # -------------------------
    # Registration Methods
    # -------------------------
    
    def register_unit(
        self,
        name: str,
        unit_id: int,
        base_unit_id: Optional[int] = None,
        **extra: Any,
    ) -> Optional[str]:
        """
        Register a created unit. Returns UUID for persistent tracking.
        """
        if not self.enabled:
            return None
        
        item_uuid = str(uuid.uuid4())[:8]
        entry: Dict[str, Any] = {
            "name": name,
            "id": unit_id,
            "uuid": item_uuid,
        }
        if base_unit_id is not None:
            entry["base_id"] = base_unit_id
        if extra:
            entry.update(extra)
        
        self.units.append(entry)
        self._uuid_map["units"][item_uuid] = unit_id
        return item_uuid
    
    def register_graphic(
        self,
        name: str,
        graphic_id: int,
        **extra: Any,
    ) -> Optional[str]:
        """Register a created graphic. Returns UUID."""
        if not self.enabled:
            return None
        
        item_uuid = str(uuid.uuid4())[:8]
        entry: Dict[str, Any] = {
            "name": name,
            "id": graphic_id,
            "uuid": item_uuid,
        }
        if extra:
            entry.update(extra)
        
        self.graphics.append(entry)
        self._uuid_map["graphics"][item_uuid] = graphic_id
        return item_uuid
    
    def register_sound(
        self,
        name: str,
        sound_id: int,
        **extra: Any,
    ) -> Optional[str]:
        """Register a created sound. Returns UUID."""
        if not self.enabled:
            return None
        
        item_uuid = str(uuid.uuid4())[:8]
        entry: Dict[str, Any] = {
            "name": name,
            "id": sound_id,
            "uuid": item_uuid,
        }
        if extra:
            entry.update(extra)
        
        self.sounds.append(entry)
        self._uuid_map["sounds"][item_uuid] = sound_id
        return item_uuid
    
    def register_tech(
        self,
        name: str,
        tech_id: int,
        effect_id: Optional[int] = None,
        **extra: Any,
    ) -> Optional[str]:
        """Register a created tech. Returns UUID."""
        if not self.enabled:
            return None
        
        item_uuid = str(uuid.uuid4())[:8]
        entry: Dict[str, Any] = {
            "name": name,
            "id": tech_id,
            "uuid": item_uuid,
        }
        if effect_id is not None:
            entry["effect_id"] = effect_id
        if extra:
            entry.update(extra)
        
        self.techs.append(entry)
        self._uuid_map["techs"][item_uuid] = tech_id
        return item_uuid
    
    def register_effect(
        self,
        name: str,
        effect_id: int,
        **extra: Any,
    ) -> Optional[str]:
        """Register a created effect. Returns UUID."""
        if not self.enabled:
            return None
        
        item_uuid = str(uuid.uuid4())[:8]
        entry: Dict[str, Any] = {
            "name": name,
            "id": effect_id,
            "uuid": item_uuid,
        }
        if extra:
            entry.update(extra)
        
        self.effects.append(entry)
        self._uuid_map["effects"][item_uuid] = effect_id
        return item_uuid
    
    # -------------------------
    # Dependency Tracking
    # -------------------------
    
    def link_dependency(
        self,
        source_type: str,
        source_id: int,
        target_type: str,
        target_id: int,
        relation: str = "references",
    ) -> None:
        """
        Register a dependency between two objects.
        
        Args:
            source_type: Type of source ("unit", "tech", "effect", etc.)
            source_id: ID of source object
            target_type: Type of target
            target_id: ID of target object
            relation: Relationship type (e.g., "uses_graphic", "links_effect")
        
        Example:
            registry.link_dependency("tech", 50, "effect", 100, "links_effect")
        """
        if not self.enabled:
            return
        
        self.dependencies.append({
            "source": f"{source_type}:{source_id}",
            "target": f"{target_type}:{target_id}",
            "relation": relation,
        })
    
    def link_tech_to_effect(self, tech_id: int, effect_id: int) -> None:
        """Convenience: link a tech to its effect."""
        self.link_dependency("tech", tech_id, "effect", effect_id, "links_effect")
    
    def link_unit_to_graphic(self, unit_id: int, graphic_id: int, graphic_type: str = "standing") -> None:
        """Convenience: link a unit to a graphic."""
        self.link_dependency("unit", unit_id, "graphic", graphic_id, f"uses_{graphic_type}_graphic")
    
    def link_unit_to_sound(self, unit_id: int, sound_id: int, sound_type: str = "selection") -> None:
        """Convenience: link a unit to a sound."""
        self.link_dependency("unit", unit_id, "sound", sound_id, f"uses_{sound_type}_sound")
    
    def get_dependencies_for(self, obj_type: str, obj_id: int) -> List[Dict[str, Any]]:
        """Get all dependencies where this object is the source."""
        key = f"{obj_type}:{obj_id}"
        return [d for d in self.dependencies if d["source"] == key]
    
    def get_dependents_of(self, obj_type: str, obj_id: int) -> List[Dict[str, Any]]:
        """Get all objects that depend on this object."""
        key = f"{obj_type}:{obj_id}"
        return [d for d in self.dependencies if d["target"] == key]
    
    # -------------------------
    # UUID-Based Lookup
    # -------------------------
    
    def get_id_by_uuid(self, obj_type: str, item_uuid: str) -> Optional[int]:
        """Get current ID for a UUID (handles ID changes)."""
        return self._uuid_map.get(obj_type, {}).get(item_uuid)
    
    def update_id(self, obj_type: str, item_uuid: str, new_id: int) -> bool:
        """Update the ID for a UUID (after object move/reindex)."""
        if obj_type in self._uuid_map and item_uuid in self._uuid_map[obj_type]:
            self._uuid_map[obj_type][item_uuid] = new_id
            # Also update in the list
            items = getattr(self, obj_type, [])
            for entry in items:
                if entry.get("uuid") == item_uuid:
                    entry["id"] = new_id
                    return True
        return False
    
    # -------------------------
    # Query Methods
    # -------------------------
    
    def get_unit_id(self, name: str) -> Optional[int]:
        """Get a unit ID by name."""
        for entry in self.units:
            if entry["name"] == name:
                return entry["id"]
        return None
    
    def get_sound_id(self, name: str) -> Optional[int]:
        """Get a sound ID by name."""
        for entry in self.sounds:
            if entry["name"] == name:
                return entry["id"]
        return None
    
    def get_graphic_id(self, name: str) -> Optional[int]:
        """Get a graphic ID by name."""
        for entry in self.graphics:
            if entry["name"] == name:
                return entry["id"]
        return None
    
    def get_tech_id(self, name: str) -> Optional[int]:
        """Get a tech ID by name."""
        for entry in self.techs:
            if entry["name"] == name:
                return entry["id"]
        return None
    
    def get_effect_id(self, name: str) -> Optional[int]:
        """Get an effect ID by name."""
        for entry in self.effects:
            if entry["name"] == name:
                return entry["id"]
        return None
    
    # -------------------------
    # Export/Import
    # -------------------------
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert registry to dictionary."""
        result: Dict[str, Any] = {}
        
        if self.units:
            result["units"] = self.units
        if self.graphics:
            result["graphics"] = self.graphics
        if self.sounds:
            result["sounds"] = self.sounds
        if self.techs:
            result["techs"] = self.techs
        if self.effects:
            result["effects"] = self.effects
        if self.dependencies:
            result["dependencies"] = self.dependencies
        
        return result
    
    def save(self, path: PathLike) -> None:
        """Save registry to a JSON file."""
        data = self.to_dict()
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    
    def load(self, path: PathLike) -> None:
        """Load registry from a JSON file."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.units = data.get("units", [])
        self.graphics = data.get("graphics", [])
        self.sounds = data.get("sounds", [])
        self.techs = data.get("techs", [])
        self.effects = data.get("effects", [])
        self.dependencies = data.get("dependencies", [])
        
        # Rebuild UUID map
        self._uuid_map = {"units": {}, "graphics": {}, "sounds": {}, "techs": {}, "effects": {}}
        for item in self.units:
            if "uuid" in item:
                self._uuid_map["units"][item["uuid"]] = item["id"]
        for item in self.graphics:
            if "uuid" in item:
                self._uuid_map["graphics"][item["uuid"]] = item["id"]
        for item in self.sounds:
            if "uuid" in item:
                self._uuid_map["sounds"][item["uuid"]] = item["id"]
        for item in self.techs:
            if "uuid" in item:
                self._uuid_map["techs"][item["uuid"]] = item["id"]
        for item in self.effects:
            if "uuid" in item:
                self._uuid_map["effects"][item["uuid"]] = item["id"]
    
    def clear(self) -> None:
        """Clear all registered items."""
        self.units.clear()
        self.graphics.clear()
        self.sounds.clear()
        self.techs.clear()
        self.effects.clear()
        self.dependencies.clear()
        self._uuid_map = {"units": {}, "graphics": {}, "sounds": {}, "techs": {}, "effects": {}}
    
    # -------------------------
    # Control
    # -------------------------
    
    def disable(self) -> None:
        """Disable auto-registration."""
        self.enabled = False
    
    def enable(self) -> None:
        """Enable auto-registration."""
        self.enabled = True
    
    # -------------------------
    # Summary
    # -------------------------
    
    def summary(self) -> str:
        """Get a summary of registered items."""
        parts = []
        if self.units:
            parts.append(f"{len(self.units)} units")
        if self.graphics:
            parts.append(f"{len(self.graphics)} graphics")
        if self.sounds:
            parts.append(f"{len(self.sounds)} sounds")
        if self.techs:
            parts.append(f"{len(self.techs)} techs")
        if self.effects:
            parts.append(f"{len(self.effects)} effects")
        if self.dependencies:
            parts.append(f"{len(self.dependencies)} deps")
        
        return ", ".join(parts) if parts else "No items registered"


# Global registry instance
registry = Registry()
