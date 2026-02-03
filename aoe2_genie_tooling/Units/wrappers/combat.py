"""
CombatWrapper - Combat/attack attribute wrapper for UnitHandle.

Ported from type_50_OLD.py to work with GenieDatParser.

Provides flat property access to CombatInfo (combat) attributes:
- Attack properties: attack_graphic_id, max_range, min_range, reload_time
- Armor properties: base_armor, displayed_attack, displayed_melee_armour
- Projectile properties: projectile_unit_id, accuracy_percent

Maps to GenieDatParser's CombatInfo structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

if TYPE_CHECKING:
    from sections.civilization.unit import Unit
    from Datasets.unit_classes import UnitClass

__all__ = ["CombatWrapper"]


class CombatWrapper:
    """
    Wrapper for CombatInfo (combat) attributes.

    Provides flat property access to all CombatInfo combat stats.
    Changes propagate to all units in the provided list.

    Attributes from GenieDatParser CombatInfo:
        base_armor, attacks, armors, defense_terrain_bonus,
        bonus_damage_resistance, max_range, blast_width, reload_time,
        projectile_unit_id, accuracy_percent, break_off_combat,
        frame_delay, weapon_offset_x/y/z, blast_attack_level,
        min_range, missed_shot_dispersion_mult, attacking_sprite_id,
        displayed_melee_armor, displayed_attack, displayed_range,
        displayed_reload_time, blast_damage, damage_reflection,
        friendly_fire_damage, interrupt_frame, garrison_firepower,
        attack_graphic2
    """

    __slots__ = ("_units",)

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_combat_info(self) -> Optional[Any]:
        """Get CombatInfo from first unit."""
        if self._units and hasattr(self._units[0], "combat_info") and self._units[0].combat_info:
            return self._units[0].combat_info
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' combat_info."""
        for unit in self._units:
            if hasattr(unit, "combat_info") and unit.combat_info:
                setattr(unit.combat_info, attr, value)

    # -------------------------
    # Attack Properties
    # -------------------------

    @property
    def attack_graphic_id(self) -> int:
        """Attack graphic ID."""
        ci = self._get_combat_info()
        return ci.attacking_sprite_id if ci else -1

    @attack_graphic_id.setter
    def attack_graphic_id(self, value: Any) -> None:
        # Accept Graphic objects or int
        if hasattr(value, "id"):
            value = value.id
        self._set_all("attacking_sprite_id", value)

    @property
    def attack_graphic_2_id(self) -> int:
        """Secondary attack graphic ID."""
        ci = self._get_combat_info()
        return ci.attack_graphic2 if ci else -1

    @attack_graphic_2_id.setter
    def attack_graphic_2_id(self, value: int) -> None:
        self._set_all("attack_graphic2", value)

    @property
    def max_range(self) -> float:
        """Maximum attack range."""
        ci = self._get_combat_info()
        return ci.max_range if ci else 0.0

    @max_range.setter
    def max_range(self, value: float) -> None:
        self._set_all("max_range", value)

    @property
    def min_range(self) -> float:
        """Minimum attack range."""
        ci = self._get_combat_info()
        return ci.min_range if ci else 0.0

    @min_range.setter
    def min_range(self, value: float) -> None:
        self._set_all("min_range", value)

    @property
    def reload_time(self) -> float:
        """Attack reload time."""
        ci = self._get_combat_info()
        return ci.reload_time if ci else 0.0

    @reload_time.setter
    def reload_time(self, value: float) -> None:
        self._set_all("reload_time", value)

    @property
    def accuracy_percent(self) -> int:
        """Attack accuracy percentage (0-100)."""
        ci = self._get_combat_info()
        return ci.accuracy_percent if ci else 0

    @accuracy_percent.setter
    def accuracy_percent(self, value: int) -> None:
        self._set_all("accuracy_percent", value)

    @property
    def accuracy_dispersion(self) -> float:
        """Attack accuracy dispersion (missed shot multiplier)."""
        ci = self._get_combat_info()
        return ci.missed_shot_dispersion_mult if ci else 0.0

    @accuracy_dispersion.setter
    def accuracy_dispersion(self, value: float) -> None:
        self._set_all("missed_shot_dispersion_mult", value)

    @property
    def blast_width(self) -> float:
        """Blast/splash damage width."""
        ci = self._get_combat_info()
        return ci.blast_width if ci else 0.0

    @blast_width.setter
    def blast_width(self, value: float) -> None:
        self._set_all("blast_width", value)

    @property
    def blast_damage(self) -> float:
        """Blast/splash damage amount."""
        ci = self._get_combat_info()
        return ci.blast_damage if ci else 0.0

    @blast_damage.setter
    def blast_damage(self, value: float) -> None:
        self._set_all("blast_damage", value)

    @property
    def blast_attack_level(self) -> int:
        """Blast attack level."""
        ci = self._get_combat_info()
        return ci.blast_attack_level if ci else 0

    @blast_attack_level.setter
    def blast_attack_level(self, value: int) -> None:
        self._set_all("blast_attack_level", value)

    @property
    def frame_delay(self) -> int:
        """Frame delay before attack hits."""
        ci = self._get_combat_info()
        return ci.frame_delay if ci else 0

    @frame_delay.setter
    def frame_delay(self, value: int) -> None:
        self._set_all("frame_delay", value)

    @property
    def break_off_combat(self) -> int:
        """Whether unit can break off combat."""
        ci = self._get_combat_info()
        return ci.break_off_combat if ci else 0

    @break_off_combat.setter
    def break_off_combat(self, value: int) -> None:
        self._set_all("break_off_combat", value)

    # -------------------------
    # Armor Properties
    # -------------------------

    @property
    def base_armor(self) -> int:
        """Base armor value."""
        ci = self._get_combat_info()
        return ci.base_armor if ci else 0

    @base_armor.setter
    def base_armor(self, value: int) -> None:
        self._set_all("base_armor", value)

    @property
    def defense_terrain_bonus(self) -> int:
        """Terrain defense bonus."""
        ci = self._get_combat_info()
        return ci.defense_terrain_bonus if ci else 0

    @defense_terrain_bonus.setter
    def defense_terrain_bonus(self, value: int) -> None:
        self._set_all("defense_terrain_bonus", value)

    @property
    def bonus_damage_resistance(self) -> float:
        """Bonus damage resistance."""
        ci = self._get_combat_info()
        return ci.bonus_damage_resistance if ci else 0.0

    @bonus_damage_resistance.setter
    def bonus_damage_resistance(self, value: float) -> None:
        self._set_all("bonus_damage_resistance", value)

    @property
    def damage_reflection(self) -> float:
        """Damage reflection amount."""
        ci = self._get_combat_info()
        return ci.damage_reflection if ci else 0.0

    @damage_reflection.setter
    def damage_reflection(self, value: float) -> None:
        self._set_all("damage_reflection", value)

    @property
    def friendly_fire_damage(self) -> float:
        """Friendly fire damage multiplier."""
        ci = self._get_combat_info()
        return ci.friendly_fire_damage if ci else 0.0

    @friendly_fire_damage.setter
    def friendly_fire_damage(self, value: float) -> None:
        self._set_all("friendly_fire_damage", value)

    # -------------------------
    # Display Properties
    # -------------------------

    @property
    def displayed_attack(self) -> int:
        """Displayed attack value in UI."""
        ci = self._get_combat_info()
        return ci.displayed_attack if ci else 0

    @displayed_attack.setter
    def displayed_attack(self, value: int) -> None:
        self._set_all("displayed_attack", value)

    @property
    def displayed_melee_armour(self) -> int:
        """Displayed melee armor in UI."""
        ci = self._get_combat_info()
        return ci.displayed_melee_armor if ci else 0

    @displayed_melee_armour.setter
    def displayed_melee_armour(self, value: int) -> None:
        self._set_all("displayed_melee_armor", value)

    @property
    def displayed_range(self) -> float:
        """Displayed range in UI."""
        ci = self._get_combat_info()
        return ci.displayed_range if ci else 0.0

    @displayed_range.setter
    def displayed_range(self, value: float) -> None:
        self._set_all("displayed_range", value)

    @property
    def displayed_reload_time(self) -> float:
        """Displayed reload time in UI."""
        ci = self._get_combat_info()
        return ci.displayed_reload_time if ci else 0.0

    @displayed_reload_time.setter
    def displayed_reload_time(self, value: float) -> None:
        self._set_all("displayed_reload_time", value)

    # -------------------------
    # Projectile Properties
    # -------------------------

    @property
    def projectile_unit_id(self) -> int:
        """Projectile unit ID."""
        ci = self._get_combat_info()
        return ci.projectile_unit_id if ci else -1

    @projectile_unit_id.setter
    def projectile_unit_id(self, value: int) -> None:
        self._set_all("projectile_unit_id", value)

    @property
    def graphic_displacement(self) -> Tuple[float, float, float]:
        """Graphic displacement (x, y, z) - weapon offset."""
        ci = self._get_combat_info()
        if ci:
            return (ci.weapon_offset_x, ci.weapon_offset_y, ci.weapon_offset_z)
        return (0.0, 0.0, 0.0)

    @graphic_displacement.setter
    def graphic_displacement(self, value: Tuple[float, float, float]) -> None:
        for unit in self._units:
            if hasattr(unit, "combat_info") and unit.combat_info:
                unit.combat_info.weapon_offset_x = value[0]
                unit.combat_info.weapon_offset_y = value[1]
                unit.combat_info.weapon_offset_z = value[2]

    @property
    def weapon_offset_x(self) -> float:
        """Weapon offset X."""
        ci = self._get_combat_info()
        return ci.weapon_offset_x if ci else 0.0

    @weapon_offset_x.setter
    def weapon_offset_x(self, value: float) -> None:
        self._set_all("weapon_offset_x", value)

    @property
    def weapon_offset_y(self) -> float:
        """Weapon offset Y."""
        ci = self._get_combat_info()
        return ci.weapon_offset_y if ci else 0.0

    @weapon_offset_y.setter
    def weapon_offset_y(self, value: float) -> None:
        self._set_all("weapon_offset_y", value)

    @property
    def weapon_offset_z(self) -> float:
        """Weapon offset Z."""
        ci = self._get_combat_info()
        return ci.weapon_offset_z if ci else 0.0

    @weapon_offset_z.setter
    def weapon_offset_z(self, value: float) -> None:
        self._set_all("weapon_offset_z", value)

    @property
    def interrupt_frame(self) -> int:
        """Interrupt frame for attack animation."""
        ci = self._get_combat_info()
        return ci.interrupt_frame if ci else 0

    @interrupt_frame.setter
    def interrupt_frame(self, value: int) -> None:
        self._set_all("interrupt_frame", value)

    @property
    def garrison_firepower(self) -> float:
        """Firepower bonus when garrisoned."""
        ci = self._get_combat_info()
        return ci.garrison_firepower if ci else 0.0

    @garrison_firepower.setter
    def garrison_firepower(self, value: float) -> None:
        self._set_all("garrison_firepower", value)

    @property
    def attacks(self) -> "AttacksManager":
        """Attacks collection manager."""
        from aoe2_genie_tooling.Units.unit_collections import AttacksManager
        return AttacksManager(self._units)

    @attacks.setter
    def attacks(self, value: List) -> None:
        """Set the entire attacks list for all units."""
        for u in self._units:
            if u.combat_info:
                u.combat_info.attacks = value

    @property
    def armours(self) -> "ArmoursManager":
        """Armours collection manager."""
        from aoe2_genie_tooling.Units.unit_collections import ArmoursManager
        return ArmoursManager(self._units)

    @armours.setter
    def armours(self, value: List) -> None:
        """Set the entire armours list for all units."""
        for u in self._units:
            if u.combat_info:
                u.combat_info.armors = value
