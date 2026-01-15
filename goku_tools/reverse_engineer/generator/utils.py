"""
Utility functions for RECodeGenerator.
"""
from __future__ import annotations
import re
from typing import Any, Dict, List, Set, Tuple
from Actual_Tools_GDP.Base.core.field_metadata import FieldReference, get_flat_fields
from .constants import SKIP_PROPERTIES, SKIP_PREFIXES

UNIT_FIELD_REFS = get_flat_fields("units")
GRAPHIC_FIELD_REFS = get_flat_fields("graphics")

TARGET_TYPE_MAP = {
    "graphichandle": "graphic",
    "soundhandle": "sound",
    "unithandle": "unit",
}

FIELD_INDEX_PATTERN = re.compile(r"\[\d+\]")


def _should_skip(name: str) -> bool:
    """Check if a property should be skipped."""
    if name in SKIP_PROPERTIES:
        return True
    for prefix in SKIP_PREFIXES:
        if name.startswith(prefix):
            return True
    return False


def safe_name(name: str) -> str:
    safe = re.sub(r'[^\w]', '_', name.lower())
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


def _candidate_field_names(field_name: str) -> List[str]:
    base = FIELD_INDEX_PATTERN.sub("", field_name)
    candidates = [base]

    if base.endswith("_id"):
        candidates.append(base[:-3])
    else:
        candidates.append(f"{base}_id")

    for suffix in (".graphic", ".sound", ".unit"):
        if base.endswith(suffix):
            candidates.append(f"{base}_id")
            candidates.append(base.replace(suffix, f"{suffix}_id"))

    seen = set()
    unique_candidates = []
    for cand in candidates:
        if cand not in seen:
            seen.add(cand)
            unique_candidates.append(cand)
    return unique_candidates


def get_field_reference(owner_type: str, field_name: str) -> FieldReference | None:
    mapping = {
        "unit": UNIT_FIELD_REFS,
        "graphic": GRAPHIC_FIELD_REFS,
    }.get(owner_type, {})

    for cand in _candidate_field_names(field_name):
        ref = mapping.get(cand)
        if ref:
            return ref
    return None


def get_field_type(field_name: str, owner_type: str | None = None) -> str:
    if owner_type:
        ref = get_field_reference(owner_type, field_name)
        if ref:
            mapped = TARGET_TYPE_MAP.get(ref.target_type.lower())
            if mapped:
                return mapped

    lower = field_name.lower()
    if "graphic" in lower or "sprite" in lower:
        return "graphic"
    elif "sound" in lower:
        return "sound"
    elif "unit" in lower or field_name in ("dead_unit_id", "blood_unit_id"):
        return "unit"
    return "unknown"


def get_null_placeholder(owner_type: str, field_name: str, fallback: int = -1) -> int:
    ref = get_field_reference(owner_type, field_name)
    if ref and isinstance(ref.null_value, int):
        return ref.null_value
    return fallback


def is_linked_field(owner_type: str, field_name: str, value: Any, config: Any) -> bool:
    if not isinstance(value, int) or value < 0:
        return False

    ftype = get_field_type(field_name, owner_type=owner_type)

    if ftype == "unit":
        min_val = getattr(config, "min_unit_ref_id", getattr(config, "min_unit_id", 0))
        return value >= min_val
    elif ftype == "graphic":
        return value >= getattr(config, "min_graphic_id", 0)
    elif ftype == "sound":
        return value >= getattr(config, "min_sound_id", 0)

    return False


def get_exportable_properties(obj: Any) -> List[Tuple[str, Any]]:
    """Extract exportable properties - only primitives (int, float, str, bool)."""
    props = []
    obj_type = type(obj)
    
    for name in dir(obj):
        if name.startswith('_'):
            continue
        
        if _should_skip(name):
            continue
        
        try:
            attr = getattr(obj_type, name, None)
            if attr is None or not isinstance(attr, property):
                val = getattr(obj, name, None)
                if callable(val):
                    continue
            else:
                val = getattr(obj, name, None)
            
            if val is None:
                continue
            
            if not isinstance(val, (int, float, str, bool)):
                continue
            
            props.append((name, val))
            
        except Exception:
            continue
    
    if hasattr(obj, "_primary_unit") and obj._primary_unit:
        for extra_attr in ["class_", "type", "unit_type"]:
            if hasattr(obj._primary_unit, extra_attr):
                try:
                    val = getattr(obj._primary_unit, extra_attr)
                    if isinstance(val, (int, float, str, bool)):
                        props.append((extra_attr, val))
                except Exception:
                    pass

    return props


def get_wrapper_properties(unit: Any, wrapper_name: str) -> List[Tuple[str, Any]]:
    """Get properties from a wrapper (type_50, dead_fish, etc.)."""
    props = []
    
    try:
        wrapper = getattr(unit, wrapper_name, None)
        if wrapper is None:
            return props
        
        for name, val in get_exportable_properties(wrapper):
            full_name = f"{wrapper_name}.{name}"
            if _should_skip(full_name):
                continue
            props.append((full_name, val))
            
    except Exception:
        pass
    
    return props
