"""
Component writers for RECodeGenerator.
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple
from .models import LinkSpec
from .utils import (
    safe_name,
    get_exportable_properties,
    get_wrapper_properties,
    get_field_type,
    get_null_placeholder,
    is_linked_field,
)


def _format_literal(val: Any) -> str:
    """Format a python literal for generated code."""
    if isinstance(val, str):
        return f'"{val}"'
    if isinstance(val, bool):
        return str(val)
    if isinstance(val, float):
        return f"{val}"
    if isinstance(val, int):
        return str(val)
    return repr(val)

def generate_collection_code(unit: Any, unit_var_name: str, config: Any) -> Tuple[List[str], List[LinkSpec]]:
    """Generate code for collections (attacks, armours, damage graphics, tasks)."""
    lines: List[str] = []
    links: List[LinkSpec] = []

    # Attacks
    if hasattr(unit, "attacks"):
        try:
            if unit.attacks:
                lines.append(f"    {unit_var_name}.attacks.clear()")
            for attack in unit.attacks:
                lines.append(
                    f"    {unit_var_name}.add_attack(class_={attack.damage_class}, amount={attack.amount})"
                )
        except Exception:
            pass

    # Armours
    if hasattr(unit, "armours"):
        try:
            if unit.armours:
                lines.append(f"    {unit_var_name}.armours.clear()")
            for armour in unit.armours:
                lines.append(
                    f"    {unit_var_name}.add_armour(class_={armour.damage_class}, amount={armour.amount})"
                )
        except Exception:
            pass

    # Damage Graphics (may reference graphics)
    if hasattr(unit, "damage_graphics"):
        try:
            if unit.damage_graphics:
                lines.append(f"    {unit_var_name}.damage_graphics.clear()")
            for idx, dmg in enumerate(unit.damage_graphics):
                g_id = getattr(dmg, "graphic_id", -1)
                placeholder_gid = g_id

                if is_linked_field("unit", "damage_graphics.graphic_id", g_id, config):
                    placeholder_gid = get_null_placeholder("unit", "damage_graphics.graphic_id", -1)
                    target_type = get_field_type("damage_graphics.graphic_id", owner_type="unit")
                    if target_type != "unknown":
                        links.append(
                            LinkSpec(
                                field=f"damage_graphics[{idx}].graphic_id",
                                target_id=g_id,
                                target_type=target_type,
                            )
                        )

                dmg_percent = getattr(dmg, "damage_percent", 0)
                apply_mode = getattr(dmg, "apply_mode", 0)
                lines.append(
                    f"    {unit_var_name}.add_damage_graphic(graphic_id={placeholder_gid}, "
                    f"damage_percent={dmg_percent}, apply_mode={apply_mode})"
                )
        except Exception:
            pass

    # Tasks (may reference graphics/sounds)
    if hasattr(unit, "tasks"):
        try:
            if unit.tasks:
                lines.append(f"    {unit_var_name}.tasks.clear()")
            for idx, task in enumerate(unit.tasks):
                args = []
                args.append(f"task_type={getattr(task, 'task_type', 1)}")

                defaults = {
                    "id": -1,
                    "is_default": False,
                    "action_type": 0,
                    "unit_class_id": -1,
                    "unit_type": -1,
                    "terrain_type": -1,
                    "resource_in": -1,
                    "resource_out": -1,
                    "work_value1": 0.0,
                    "work_value2": 0.0,
                    "work_range": 0.0,
                }

                for field, default_val in defaults.items():
                    val = getattr(task, field, None)
                    if val is None or val == default_val:
                        continue

                    full_field_name = f"tasks.{field}"
                    if is_linked_field("unit", full_field_name, val, config):
                        placeholder = get_null_placeholder("unit", full_field_name, default_val)
                        target_type = get_field_type(full_field_name, owner_type="unit")
                        if target_type != "unknown":
                            links.append(
                                LinkSpec(
                                    field=f"tasks[{idx}].{field}",
                                    target_id=val,
                                    target_type=target_type,
                                )
                            )
                        args.append(f"{field}={_format_literal(placeholder)}")
                    else:
                        args.append(f"{field}={_format_literal(val)}")

                lines.append(f"    {unit_var_name}.tasks.add({', '.join(args)})")
        except Exception:
            pass

    return lines, links

def generate_unit_code(ws: Any, unit_id: int, group: Any, config: Any) -> Tuple[List[str], List[LinkSpec]]:
    """Generate Python code for a single unit."""
    try:
        unit = ws.unit_manager.get(unit_id)
    except Exception:
        return [f"    # Unit {unit_id} not found"], []

    if unit is None or unit._primary_unit is None:
        return [f"    # Unit {unit_id} not found"], []

    name = getattr(unit, "name", f"Unit_{unit_id}")
    unit_safe_name = safe_name(name)

    links_to_apply: List[LinkSpec] = []

    lines = [
        f"",
        f"def create_unit_{unit_id}_{unit_safe_name}(ws):",
        f'    """Create {name} (ID: {unit_id})"""',
        f'    print(f"      - Unit: {name} (ID: {unit_id})")',
        f'    unit = ws.unit_manager.create("{name}")',
        f"",
    ]

    base_props = get_exportable_properties(unit)

    for wrapper in ["type_50", "dead_fish", "bird", "creatable", "building"]:
        base_props.extend(get_wrapper_properties(unit, wrapper))

    for prop_name, val in sorted(base_props, key=lambda x: x[0]):
        if prop_name in ("id", "unit_id"):
            continue

        if is_linked_field("unit", prop_name, val, config):
            target_type = get_field_type(prop_name, owner_type="unit")
            if target_type != "unknown":
                links_to_apply.append(
                    LinkSpec(field=prop_name, target_id=val, target_type=target_type)
                )
                continue

        if isinstance(val, int) and val == -1:
            continue

        formatted = _format_literal(val)

        if "." in prop_name:
            parts = prop_name.split(".")
            setter = f"unit.{parts[0]}.{parts[1]}"
        else:
            setter = f"unit.{prop_name}"

        lines.append(f"    {setter} = {formatted}")

    collection_lines, collection_links = generate_collection_code(unit, "unit", config)
    lines.extend(collection_lines)
    links_to_apply.extend(collection_links)

    lines.append("")
    lines.append("    return unit")
    lines.append("")

    return lines, links_to_apply

def generate_graphic_code(ws: Any, graphic_id: int, group: Any, config: Any) -> Tuple[List[str], List[LinkSpec]]:
    """Generate Python code for a single graphic."""
    try:
        graphic = ws.graphic_manager.get(graphic_id)
    except Exception:
        return [f"    # Graphic {graphic_id} not found"], []

    name = getattr(graphic, "name", f"Graphic_{graphic_id}")
    graphic_safe_name = safe_name(name)

    links_to_apply: List[LinkSpec] = []

    lines = [
        f"",
        f"def create_graphic_{graphic_id}_{graphic_safe_name}(ws):",
        f'    """Create Graphic {graphic_id} ({name})"""',
        f'    print(f"      - Graphic: {name} (ID: {graphic_id})")',
        f'    graphic = ws.graphic_manager.add_graphic("{name}")',
        f"",
    ]

    props = get_exportable_properties(graphic)

    for prop_name, val in sorted(props, key=lambda x: x[0]):
        if prop_name in ("id", "deltas", "num_deltas"):
            continue

        if is_linked_field("graphic", prop_name, val, config):
            target_type = get_field_type(prop_name, owner_type="graphic")
            if target_type != "unknown":
                links_to_apply.append(
                    LinkSpec(field=prop_name, target_id=val, target_type=target_type)
                )
                continue

        lines.append(f"    graphic.{prop_name} = {_format_literal(val)}")

    if hasattr(graphic, "deltas"):
        try:
            for idx, delta in enumerate(graphic.deltas):
                g_id = int(delta.graphic_id) if delta.graphic_id is not None else -1
                off_x = int(delta.offset_x)
                off_y = int(delta.offset_y)
                disp_a = int(delta.display_angle)

                placeholder_gid = g_id
                if is_linked_field("graphic", "deltas.graphic", g_id, config):
                    placeholder_gid = get_null_placeholder("graphic", "deltas.graphic", -1)
                    target_type = get_field_type("deltas.graphic", owner_type="graphic")
                    if target_type != "unknown":
                        links_to_apply.append(
                            LinkSpec(
                                field=f"deltas[{idx}].graphic_id",
                                target_id=g_id,
                                target_type=target_type,
                            )
                        )

                lines.append(
                    f"    graphic.add_delta(graphic_id={placeholder_gid}, "
                    f"offset_x={off_x}, offset_y={off_y}, display_angle={disp_a})"
                )
        except Exception:
            pass

    lines.append("")
    lines.append("    return graphic")
    lines.append("")

    return lines, links_to_apply

def generate_sound_code(ws: Any, sound_id: int, group: Any, config: Any) -> Tuple[List[str], List[LinkSpec]]:
    """Generate Python code for a single sound container."""
    try:
        sound = ws.sound_manager.get(sound_id)
    except Exception:
        return [f"    # Sound {sound_id} not found"], []

    sound_name = f"sound_{sound_id}"
    try:
        sound_files = sound.sounds if hasattr(sound, 'sounds') else []
        if sound_files:
            first_file = sound_files[0]
            if hasattr(first_file, 'sound_name') and first_file.sound_name:
                sound_name = first_file.sound_name
            elif hasattr(first_file, 'filename') and first_file.filename:
                sound_name = first_file.filename
    except Exception:
        pass

    sound_safe_name = safe_name(sound_name)
    links_to_apply: List[LinkSpec] = []

    lines = [
        f"",
        f"def create_sound_{sound_id}_{sound_safe_name}(ws):",
        f'    """Create Sound {sound_id} ({sound_name})"""',
        f'    print(f"      - Sound: {sound_name} (ID: {sound_id})")',
        f'    sound = ws.sound_manager.add_new()',
        f"",
    ]

    props = get_exportable_properties(sound)
    for prop_name, val in sorted(props, key=lambda x: x[0]):
        if prop_name in ("id", "num_sound_files", "sound_files"):
            continue
        lines.append(f"    sound.{prop_name} = {_format_literal(val)}")

    try:
        sound_files = sound.sounds if hasattr(sound, 'sounds') else []
        for i, sf in enumerate(sound_files):
            sf_props = get_exportable_properties(sf)
            sf_args = []
            for prop_name, val in sf_props:
                if prop_name in ("index", "id"):
                    continue
                if isinstance(val, str) and val:
                    sf_args.append(f'{prop_name}="{val}"')
                elif isinstance(val, float):
                    sf_args.append(f'{prop_name}={val}')
                elif isinstance(val, int) and val >= 0:
                    sf_args.append(f'{prop_name}={val}')

            if sf_args:
                lines.append(f"    sound.new_sound({', '.join(sf_args)})")
            else:
                lines.append(f"    sound.new_sound()")
    except Exception:
        pass

    lines.append("")
    lines.append("    return sound")
    lines.append("")

    return lines, links_to_apply


# ===== INDEPENDENT OBJECT WRITERS =====
# These hard-code ALL values - no deferred linking

def generate_independent_unit_code(ws: Any, unit_id: int, config: Any) -> List[str]:
    """Generate Python code for an independent unit (all values hard-coded)."""
    try:
        unit = ws.unit_manager.get(unit_id)
    except Exception:
        return [f"    # Unit {unit_id} not found"]

    if unit is None or unit._primary_unit is None:
        return [f"    # Unit {unit_id} not found"]

    name = getattr(unit, "name", f"Unit_{unit_id}")
    unit_safe_name = safe_name(name)

    lines = [
        f"",
        f"def create_unit_{unit_id}_{unit_safe_name}(ws):",
        f'    """Create {name} (ID: {unit_id}) - Independent"""',
        f'    print(f"      - Unit: {name} (ID: {unit_id})")',
        f'    unit = ws.unit_manager.create("{name}")',
        f"",
    ]

    base_props = get_exportable_properties(unit)

    for wrapper in ["type_50", "dead_fish", "bird", "creatable", "building"]:
        base_props.extend(get_wrapper_properties(unit, wrapper))

    for prop_name, val in sorted(base_props, key=lambda x: x[0]):
        if prop_name in ("id", "unit_id"):
            continue

        # Skip -1 values
        if isinstance(val, int) and val == -1:
            continue

        formatted = _format_literal(val)

        if "." in prop_name:
            parts = prop_name.split(".")
            setter = f"unit.{parts[0]}.{parts[1]}"
        else:
            setter = f"unit.{prop_name}"

        lines.append(f"    {setter} = {formatted}")

    # Collections - all hard-coded
    if hasattr(unit, "attacks"):
        try:
            for attack in unit.attacks:
                lines.append(
                    f"    unit.add_attack(class_={attack.damage_class}, amount={attack.amount})"
                )
        except Exception:
            pass

    if hasattr(unit, "armours"):
        try:
            for armour in unit.armours:
                lines.append(
                    f"    unit.add_armour(class_={armour.damage_class}, amount={armour.amount})"
                )
        except Exception:
            pass

    if hasattr(unit, "damage_graphics"):
        try:
            for dmg in unit.damage_graphics:
                g_id = getattr(dmg, "graphic_id", -1)
                dmg_percent = getattr(dmg, "damage_percent", 0)
                apply_mode = getattr(dmg, "apply_mode", 0)
                lines.append(
                    f"    unit.add_damage_graphic(graphic_id={g_id}, "
                    f"damage_percent={dmg_percent}, apply_mode={apply_mode})"
                )
        except Exception:
            pass

    lines.append("")
    lines.append("    return unit")
    lines.append("")

    return lines


def generate_independent_graphic_code(ws: Any, graphic_id: int, config: Any) -> List[str]:
    """Generate Python code for an independent graphic (all values hard-coded)."""
    try:
        graphic = ws.graphic_manager.get(graphic_id)
    except Exception:
        return [f"    # Graphic {graphic_id} not found"]

    name = getattr(graphic, "name", f"Graphic_{graphic_id}")
    graphic_safe_name = safe_name(name)

    lines = [
        f"",
        f"def create_graphic_{graphic_id}_{graphic_safe_name}(ws):",
        f'    """Create Graphic {graphic_id} ({name}) - Independent"""',
        f'    print(f"      - Graphic: {name} (ID: {graphic_id})")',
        f'    graphic = ws.graphic_manager.add_graphic("{name}")',
        f"",
    ]

    props = get_exportable_properties(graphic)

    for prop_name, val in sorted(props, key=lambda x: x[0]):
        if prop_name in ("id", "deltas", "num_deltas"):
            continue
        lines.append(f"    graphic.{prop_name} = {_format_literal(val)}")

    if hasattr(graphic, "deltas"):
        try:
            for delta in graphic.deltas:
                g_id = int(delta.graphic_id) if delta.graphic_id is not None else -1
                off_x = int(delta.offset_x)
                off_y = int(delta.offset_y)
                disp_a = int(delta.display_angle)
                lines.append(
                    f"    graphic.add_delta(graphic_id={g_id}, "
                    f"offset_x={off_x}, offset_y={off_y}, display_angle={disp_a})"
                )
        except Exception:
            pass

    lines.append("")
    lines.append("    return graphic")
    lines.append("")

    return lines


def generate_independent_sound_code(ws: Any, sound_id: int, config: Any) -> List[str]:
    """Generate Python code for an independent sound (all values hard-coded)."""
    try:
        sound = ws.sound_manager.get(sound_id)
    except Exception:
        return [f"    # Sound {sound_id} not found"]

    sound_name = f"sound_{sound_id}"
    try:
        sound_files = sound.sounds if hasattr(sound, 'sounds') else []
        if sound_files:
            first_file = sound_files[0]
            if hasattr(first_file, 'sound_name') and first_file.sound_name:
                sound_name = first_file.sound_name
            elif hasattr(first_file, 'filename') and first_file.filename:
                sound_name = first_file.filename
    except Exception:
        pass

    sound_safe_name = safe_name(sound_name)

    lines = [
        f"",
        f"def create_sound_{sound_id}_{sound_safe_name}(ws):",
        f'    """Create Sound {sound_id} ({sound_name}) - Independent"""',
        f'    print(f"      - Sound: {sound_name} (ID: {sound_id})")',
        f'    sound = ws.sound_manager.add_new()',
        f"",
    ]

    props = get_exportable_properties(sound)
    for prop_name, val in sorted(props, key=lambda x: x[0]):
        if prop_name in ("id", "num_sound_files", "sound_files"):
            continue
        lines.append(f"    sound.{prop_name} = {_format_literal(val)}")

    try:
        sound_files = sound.sounds if hasattr(sound, 'sounds') else []
        for sf in sound_files:
            sf_props = get_exportable_properties(sf)
            sf_args = []
            for prop_name, val in sf_props:
                if prop_name in ("index", "id"):
                    continue
                if isinstance(val, str) and val:
                    sf_args.append(f'{prop_name}="{val}"')
                elif isinstance(val, float):
                    sf_args.append(f'{prop_name}={val}')
                elif isinstance(val, int) and val >= 0:
                    sf_args.append(f'{prop_name}={val}')

            if sf_args:
                lines.append(f"    sound.new_sound({', '.join(sf_args)})")
            else:
                lines.append(f"    sound.new_sound()")
    except Exception:
        pass

    lines.append("")
    lines.append("    return sound")
    lines.append("")

    return lines

