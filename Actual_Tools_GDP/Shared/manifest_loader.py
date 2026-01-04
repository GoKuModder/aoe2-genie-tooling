"""
ManifestLoader and TwoPassSerializer - Dynamic attribute validation.

This module provides:
- ManifestLoader: Loads manifest.csv and provides validation rules
- DeferredReference: Stores UUID-based references with source tracking
- TwoPassSerializer: Validates all deferred references at save time

Usage:
    from Actual_Tools_GDP.Shared.manifest_loader import manifest, DeferredReference
    
    # Set a reference attribute - accepts int or Handle
    unit.standing_graphic = 1000  # int - validated at save
    unit.standing_graphic = some_graphic  # GraphicHandle - validated at save
    
    # Final validation happens at workspace.save()
"""
from __future__ import annotations

import csv
import traceback
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from genieutils.datfile import DatFile

__all__ = [
    "manifest",
    "ManifestLoader",
    "DeferredReference",
    "ValidationError",
    "ReferenceNotFoundError",
    "EnumValueError",
    "CircularReferenceError",
    "DuplicateIdError",
]


# =============================================================================
# EXCEPTIONS
# =============================================================================

class ValidationError(Exception):
    """Base validation error with source tracking."""
    
    def __init__(self, message: str, source_info: Optional[str] = None):
        self.source_info = source_info
        full_msg = message
        if source_info:
            full_msg = f"{message}\n  Source: {source_info}"
        super().__init__(full_msg)


class ReferenceNotFoundError(ValidationError):
    """Raised when a referenced ID doesn't exist at save time."""
    pass


class EnumValueError(ValidationError):
    """Raised when a value is not valid for an enum."""
    pass


class CircularReferenceError(ValidationError):
    """Raised when circular references are detected (A→B→A)."""
    pass


class DuplicateIdError(ValidationError):
    """Raised when the same ID is used for multiple objects."""
    pass


# =============================================================================
# DEFERRED REFERENCE
# =============================================================================

@dataclass
class DeferredReference:
    """
    Stores a reference that will be validated at save time.
    
    Captures the source location (file/line) for error reporting.
    """
    target_type: str  # "UnitHandle", "GraphicHandle", "SoundHandle", "TechHandle"
    value: Union[int, str]  # int ID or UUID string
    source_file: str = ""
    source_line: int = 0
    source_code: str = ""
    attribute_name: str = ""
    
    @classmethod
    def create(cls, target_type: str, value: Union[int, str], attr_name: str) -> "DeferredReference":
        """Create with automatic source tracking."""
        # Get caller's stack frame
        stack = traceback.extract_stack()
        # Skip internal frames, find user code
        for frame in reversed(stack[:-2]):  # Skip this method and caller
            if "site-packages" not in frame.filename and "Actual_Tools" not in frame.filename:
                return cls(
                    target_type=target_type,
                    value=value,
                    source_file=frame.filename,
                    source_line=frame.lineno,
                    source_code=frame.line or "",
                    attribute_name=attr_name,
                )
        # Fallback to direct caller
        frame = stack[-3] if len(stack) >= 3 else stack[-1]
        return cls(
            target_type=target_type,
            value=value,
            source_file=frame.filename,
            source_line=frame.lineno,
            source_code=frame.line or "",
            attribute_name=attr_name,
        )
    
    def format_source(self) -> str:
        """Format source info for error messages."""
        return f"{self.source_file}:{self.source_line} - {self.source_code.strip()}"


# =============================================================================
# MANIFEST ENTRY
# =============================================================================

@dataclass
class ManifestEntry:
    """A single attribute definition from manifest.csv."""
    id: int
    name: str
    storage_type: str  # "Value", "Reference", "Bitmask", "Enum"
    link_target: str  # "None", "UnitHandle", "GraphicHandle", etc.
    data_type: str  # "int", "float", "tuple"
    description: str
    
    @property
    def is_reference(self) -> bool:
        return self.storage_type == "Reference"
    
    @property
    def is_enum(self) -> bool:
        return self.storage_type in ("Enum", "Bitmask")
    
    @property
    def enum_name(self) -> Optional[str]:
        """Extract enum class name from link_target like 'Enum:GarrisonType'."""
        if self.link_target.startswith("Enum:"):
            return self.link_target[5:]
        return None


# =============================================================================
# MANIFEST LOADER
# =============================================================================

class ManifestLoader:
    """
    Loads and provides access to attribute manifest.
    
    The manifest defines storage types and validation rules for each attribute.
    """
    
    def __init__(self, manifest_path: Optional[Path] = None):
        self.entries: Dict[int, ManifestEntry] = {}
        self.entries_by_name: Dict[str, ManifestEntry] = {}
        self._enum_classes: Dict[str, Type[IntEnum]] = {}
        self._loaded = False
        self._manifest_path = manifest_path
    
    def load(self, path: Optional[Path] = None) -> None:
        """Load manifest.csv from disk."""
        if path is None:
            path = self._manifest_path or Path(__file__).parent.parent.parent / "Datasets" / "manifest.csv"
        
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {path}")
        
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entry = ManifestEntry(
                    id=int(row['ID']),
                    name=row['Name'],
                    storage_type=row['Storage_Type'],
                    link_target=row['Link_Target'],
                    data_type=row['Data_Type'],
                    description=row['Description'],
                )
                self.entries[entry.id] = entry
                self.entries_by_name[entry.name] = entry
        
        self._loaded = True
        self._load_enum_classes()
    
    def _load_enum_classes(self) -> None:
        """Load all enum classes from attributes module."""
        try:
            from Datasets import attributes
            for name in dir(attributes):
                obj = getattr(attributes, name)
                if isinstance(obj, type) and issubclass(obj, IntEnum) and obj is not IntEnum:
                    self._enum_classes[name] = obj
        except ImportError:
            pass  # Enums not available
    
    def get(self, attr_id: int) -> Optional[ManifestEntry]:
        """Get manifest entry by attribute ID."""
        if not self._loaded:
            self.load()
        return self.entries.get(attr_id)
    
    def get_by_name(self, name: str) -> Optional[ManifestEntry]:
        """Get manifest entry by attribute name."""
        if not self._loaded:
            self.load()
        return self.entries_by_name.get(name.upper())
    
    def get_enum_class(self, name: str) -> Optional[Type[IntEnum]]:
        """Get an enum class by name."""
        if not self._loaded:
            self.load()
        return self._enum_classes.get(name)
    
    def validate_enum_value(self, entry: ManifestEntry, value: int, source_info: Optional[str] = None) -> None:
        """
        Validate a value against an enum immediately.
        
        Args:
            entry: Manifest entry for the attribute
            value: Value to validate
            source_info: Optional source location (file:line - code)
        
        Raises:
            EnumValueError: If value is not valid, with detailed message
        """
        if not entry.is_enum:
            return
        
        enum_name = entry.enum_name
        if not enum_name:
            return
        
        enum_class = self.get_enum_class(enum_name)
        if not enum_class:
            return  # Enum class not found, skip validation
        
        # Build valid values list (dynamic introspection, not hardcoded)
        valid_values_list = [f"{e.name}={e.value}" for e in enum_class]
        
        # For bitmask enums, check if value is a valid combination
        if entry.storage_type == "Bitmask":
            valid_flags = sum(e.value for e in enum_class if e.value > 0)
            if value < 0 or (value & ~valid_flags) != 0:
                msg = f"{entry.name}: Invalid bitmask value {value} for {enum_name}.\n"
                msg += f"  Valid flags: {', '.join(valid_values_list)}\n"
                msg += f"  Combine using bitwise OR (|)"
                raise EnumValueError(msg, source_info)
        else:
            # For regular enums, check if value exists (get valid values dynamically)
            valid_values_set = {e.value for e in enum_class}
            if value not in valid_values_set:
                msg = f"{entry.name}: Invalid value {value} for {enum_name}.\n"
                msg += f"  Valid values: {', '.join(valid_values_list)}"
                raise EnumValueError(msg, source_info)


# =============================================================================
# TWO PASS SERIALIZER
# =============================================================================

class TwoPassSerializer:
    """
    Collects deferred references and validates them at save time.
    
    Pass 1: Collect all references during attribute assignment
    Pass 2: Validate all references exist when saving
    """
    
    def __init__(self):
        self.deferred_refs: List[DeferredReference] = []
        self.validators: Dict[str, Callable[[int, DatFile], bool]] = {}
        self._setup_validators()
    
    def _setup_validators(self) -> None:
        """Setup validation functions for each reference type."""
        self.validators = {
            "UnitHandle": self._validate_unit,
            "GraphicHandle": self._validate_graphic,
            "SoundHandle": self._validate_sound,
            "TechHandle": self._validate_tech,
            "EffectHandle": self._validate_effect,
            "TerrainType": self._validate_terrain,
            "TerrainTable": self._validate_terrain_table,
        }
    
    def add_deferred(self, ref: DeferredReference) -> None:
        """Add a deferred reference to validate later."""
        self.deferred_refs.append(ref)
    
    def clear(self) -> None:
        """Clear all deferred references."""
        self.deferred_refs.clear()
    
    def check_duplicates(self, dat_file: "DatFile") -> List[ValidationError]:
        """
        Check for duplicate ID usage within each category.
        
        Detects:
        - Multiple units with the same ID
        - Multiple graphics with the same ID
        - etc.
        
        Returns list of DuplicateIdError (empty if no duplicates).
        """
        errors: List[ValidationError] = []
        
        # Check units (same ID in multiple civs is OK, but None gaps are checked)
        # Units are special - they exist in each civ's unit list
        # For now, we check if registry has duplicate names mapped to same ID
        from .registry import registry
        
        # Check for duplicate unit names
        unit_names: Dict[str, List[int]] = {}
        for entry in registry.units:
            name = entry.get("name", "")
            uid = entry.get("id", -1)
            if name:
                if name not in unit_names:
                    unit_names[name] = []
                unit_names[name].append(uid)
        
        for name, ids in unit_names.items():
            if len(ids) > 1 and len(set(ids)) > 1:
                errors.append(DuplicateIdError(
                    f"Unit name '{name}' is registered with multiple IDs: {ids}"
                ))
        
        # Check for duplicate IDs with different names
        unit_ids: Dict[int, List[str]] = {}
        for entry in registry.units:
            name = entry.get("name", "")
            uid = entry.get("id", -1)
            if uid >= 0:
                if uid not in unit_ids:
                    unit_ids[uid] = []
                unit_ids[uid].append(name)
        
        for uid, names in unit_ids.items():
            unique_names = set(names)
            if len(unique_names) > 1:
                errors.append(DuplicateIdError(
                    f"Unit ID {uid} is used by multiple units: {list(unique_names)}"
                ))
        
        return errors
    
    def check_circular_references(self, dat_file: "DatFile") -> List[ValidationError]:
        """
        Check for circular references between units.
        
        Detects patterns like:
        - Unit A's dead_unit_id → Unit B, and Unit B's dead_unit_id → Unit A
        - Unit A → Unit B → Unit C → Unit A (chains)
        
        Returns list of CircularReferenceError (empty if no cycles).
        """
        errors: List[ValidationError] = []
        
        if not dat_file.civs:
            return errors
        
        units = dat_file.civs[0].units
        
        # Build reference graph for each reference type
        reference_fields = [
            ("dead_unit_id", "dead_unit_id"),
            ("tracking_unit", "dead_fish.tracking_unit"),
        ]
        
        for field_name, path in reference_fields:
            # Build adjacency list
            graph: Dict[int, int] = {}
            for i, unit in enumerate(units):
                if unit is None:
                    continue
                
                # Get the reference value
                try:
                    ref_id = getattr(unit, field_name, -1)
                    if ref_id is None:
                        ref_id = -1
                except:
                    ref_id = -1
                
                # Skip self-references (unit pointing to itself is OK)
                # Only add to graph if it points to a DIFFERENT unit
                if ref_id >= 0 and ref_id < len(units) and ref_id != i:
                    graph[i] = ref_id
            
            # Detect cycles using DFS
            visited: Set[int] = set()
            rec_stack: Set[int] = set()
            
            def find_cycle(node: int, path: List[int]) -> Optional[List[int]]:
                """DFS to find cycles. Returns cycle path if found."""
                if node in rec_stack:
                    # Found cycle - extract the cycle portion
                    cycle_start = path.index(node)
                    return path[cycle_start:] + [node]
                
                if node in visited:
                    return None
                
                visited.add(node)
                rec_stack.add(node)
                path.append(node)
                
                if node in graph:
                    next_node = graph[node]
                    cycle = find_cycle(next_node, path)
                    if cycle:
                        return cycle
                
                path.pop()
                rec_stack.remove(node)
                return None
            
            # Check each node
            for start_node in graph.keys():
                if start_node not in visited:
                    cycle = find_cycle(start_node, [])
                    if cycle:
                        # Format cycle for error message
                        cycle_str = " → ".join(str(u) for u in cycle)
                        errors.append(CircularReferenceError(
                            f"Circular reference detected in '{field_name}': {cycle_str}"
                        ))
                        # Only report first cycle per field
                        break
        
        return errors
    
    def validate_all(self, dat_file: "DatFile") -> List[ValidationError]:
        """
        Validate all deferred references against the DatFile.
        
        Checks performed:
        1. Reference existence (IDs must exist)
        2. Duplicate ID detection
        3. Circular reference detection
        
        Returns list of errors (empty if all valid).
        """
        errors: List[ValidationError] = []
        
        # Check for duplicates first
        errors.extend(self.check_duplicates(dat_file))
        
        # Check for circular references
        errors.extend(self.check_circular_references(dat_file))
        
        # Validate deferred references
        for ref in self.deferred_refs:
            validator = self.validators.get(ref.target_type)
            if validator is None:
                continue  # Unknown type, skip
            
            # Get the actual ID value
            if isinstance(ref.value, str):
                # UUID - need to look up in registry
                from .registry import registry
                actual_id = registry.get_id_by_uuid(
                    ref.target_type.lower().replace("handle", "s"), 
                    ref.value
                )
                if actual_id is None:
                    errors.append(ReferenceNotFoundError(
                        f"UUID '{ref.value}' for {ref.target_type} not found in registry",
                        ref.format_source()
                    ))
                    continue
            else:
                actual_id = ref.value
            
            # Skip -1 (means "none")
            if actual_id < 0:
                continue
            
            # Validate the ID exists and build detailed error with context
            if not validator(actual_id, dat_file):
                # Get size context for better error messages
                context = self._get_reference_context(ref.target_type, dat_file)
                
                msg = f"{ref.attribute_name}: {ref.target_type} ID {actual_id} does not exist\n"
                if context:
                    msg += f"  {context}\n"
                
                errors.append(ReferenceNotFoundError(msg.strip(), ref.format_source()))
        
        return errors
    
    def _get_reference_context(self, target_type: str, dat: "DatFile") -> str:
        """Get contextual information about valid ID ranges for a reference type."""
        try:
            if target_type == "UnitHandle" and dat.civs:
                total = len(dat.civs[0].units)
                return f"Total units in DAT: {total}, valid range: 0-{total-1}"
            elif target_type == "GraphicHandle":
                total = len(dat.graphics)
                return f"Total graphics in DAT: {total}, valid range: 0-{total-1}"
            elif target_type == "SoundHandle":
                total = len(dat.sounds)
                return f"Total sounds in DAT: {total}, valid range: 0-{total-1}"
            elif target_type == "TechHandle":
                total = len(dat.techs)
                return f"Total techs in DAT: {total}, valid range: 0-{total-1}"
            elif target_type == "EffectHandle":
                total = len(dat.effects)
                return f"Total effects in DAT: {total}, valid range: 0-{total-1}"
            elif target_type in ("TerrainType", "TerrainTable"):
                return "Valid range: 0-99 (terrain IDs)"
        except:
            pass
        return ""
    
    # Validator implementations
    def _validate_unit(self, unit_id: int, dat: "DatFile") -> bool:
        if not dat.civs:
            return True
        return 0 <= unit_id < len(dat.civs[0].units) and dat.civs[0].units[unit_id] is not None
    
    def _validate_graphic(self, gfx_id: int, dat: "DatFile") -> bool:
        return 0 <= gfx_id < len(dat.graphics) and dat.graphics[gfx_id] is not None
    
    def _validate_sound(self, sound_id: int, dat: "DatFile") -> bool:
        return 0 <= sound_id < len(dat.sounds) and dat.sounds[sound_id] is not None
    
    def _validate_tech(self, tech_id: int, dat: "DatFile") -> bool:
        return 0 <= tech_id < len(dat.techs) and dat.techs[tech_id] is not None
    
    def _validate_effect(self, effect_id: int, dat: "DatFile") -> bool:
        return 0 <= effect_id < len(dat.effects) and dat.effects[effect_id] is not None
    
    def _validate_terrain(self, terrain_id: int, dat: "DatFile") -> bool:
        # Terrains are usually 0-100 range
        return 0 <= terrain_id < 100
    
    def _validate_terrain_table(self, table_id: int, dat: "DatFile") -> bool:
        # Terrain restriction tables
        return 0 <= table_id < len(dat.terrain_restrictions) if hasattr(dat, 'terrain_restrictions') else True


# =============================================================================
# GLOBAL INSTANCES
# =============================================================================

manifest = ManifestLoader()
serializer = TwoPassSerializer()
