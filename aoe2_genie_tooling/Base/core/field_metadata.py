"""
Field Metadata Registry - Loads from field_discovery.json.

This module provides typed access to reference field metadata for validation.
The JSON file is the source of truth for all reference fields.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import json

__all__ = ["FieldReference", "load_field_metadata", "FIELD_METADATA"]


@dataclass
class FieldReference:
    """Metadata about a field that references another object."""
    target_type: str
    manager_name: Optional[str]
    nullable: bool = True
    null_value: int = -1
    description: str = ""


def load_field_metadata() -> Dict[str, Dict[str, Dict[str, FieldReference]]]:
    """
    Load field metadata from JSON file.
    
    Returns:
        {
            "units": {"graphics": {"standing_graphic": FieldReference(...), ...}, ...},
            "techs": {...},
            "graphics": {...}
        }
    """
    json_path = Path(__file__).parent / "field_discovery.json"
    
    with open(json_path, "r") as f:
        raw = json.load(f)
    
    result = {}
    
    for obj_type, categories in raw.items():
        result[obj_type] = {}
        for category, fields in categories.items():
            result[obj_type][category] = {}
            for field_name, field_data in fields.items():
                result[obj_type][category][field_name] = FieldReference(
                    target_type=field_data["target"],
                    manager_name=field_data.get("manager"),
                    nullable=field_data.get("nullable", True),
                    null_value=field_data.get("null_value", -1),
                )
    
    return result


def get_flat_fields(obj_type: str) -> Dict[str, FieldReference]:
    """
    Get all fields for an object type as a flat dictionary.
    
    Args:
        obj_type: "units", "techs", or "graphics"
        
    Returns:
        {"field_name": FieldReference(...), ...}
    """
    result = {}
    if obj_type not in FIELD_METADATA:
        return result
    
    for category, fields in FIELD_METADATA[obj_type].items():
        result.update(fields)
    
    return result


# Load on module import
FIELD_METADATA = load_field_metadata()

# Convenience accessors
UNIT_FIELDS = get_flat_fields("units")
TECH_FIELDS = get_flat_fields("techs")
GRAPHIC_FIELDS = get_flat_fields("graphics")
