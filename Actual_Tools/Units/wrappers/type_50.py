"""
Type50Wrapper - Combat/attack attribute wrapper for UnitHandle.

Provides flat property access to Type50 (combat) attributes:
- Attack properties: attack_graphic, max_range, min_range, reload_time
- Armor properties: base_armor, displayed_attack, displayed_melee_armour
- Projectile properties: projectile_unit_id, accuracy_percent

Mirrors genieutils.unit.Type50 structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from genieutils.unit import Unit
    from Datasets.unit_classes import UnitClass

__all__ = ["Type50Wrapper"]


class Type50Wrapper:
    """
    Wrapper for Type50 (combat) attributes.
    
    Provides flat property access to all Type50 combat stats.
    Changes propagate to all units in the provided list.
    
    Attributes from genieutils.unit.Type50:
        base_armor, attacks, armours, defense_terrain_bonus,
        bonus_damage_resistance, max_range, blast_width, reload_time,
        projectile_unit_id, accuracy_percent, break_off_combat,
        frame_delay, graphic_displacement, blast_attack_level,
        min_range, accuracy_dispersion, attack_graphic,
        displayed_melee_armour, displayed_attack, displayed_range,
        displayed_reload_time, blast_damage, damage_reflection,
        friendly_fire_damage, interrupt_frame, garrison_firepower,
        attack_graphic_2
    """
    
    __slots__ = ("_units",)
    
    def __init__(self, units: List[Unit]) -> None:
        """
        Initialize with list of units to modify.
        
        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)
    
    def _get_type50(self) -> Optional[Any]:
        """Get Type50 from first unit."""
        if self._units and self._units[0].type_50:
            return self._units[0].type_50
        return None
    
    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' type_50."""
        for unit in self._units:
            if unit.type_50:
                setattr(unit.type_50, attr, value)
    
    # -------------------------
    # Attack Properties
    # -------------------------
    
    @property
    def attack_graphic(self) -> int:
        """Attack graphic ID."""
        t50 = self._get_type50()
        return t50.attack_graphic if t50 else -1
    
    @attack_graphic.setter
    def attack_graphic(self, value: Any) -> None:
        # Accept Graphic objects or int
        if hasattr(value, "id"):
            value = value.id
        self._set_all("attack_graphic", value)
    
    @property
    def attack_graphic_2(self) -> int:
        """Secondary attack graphic ID."""
        t50 = self._get_type50()
        return t50.attack_graphic_2 if t50 else -1
    
    @attack_graphic_2.setter
    def attack_graphic_2(self, value: int) -> None:
        self._set_all("attack_graphic_2", value)
    
    @property
    def max_range(self) -> float:
        """Maximum attack range."""
        t50 = self._get_type50()
        return t50.max_range if t50 else 0.0
    
    @max_range.setter
    def max_range(self, value: float) -> None:
        self._set_all("max_range", value)
    
    @property
    def min_range(self) -> float:
        """Minimum attack range."""
        t50 = self._get_type50()
        return t50.min_range if t50 else 0.0
    
    @min_range.setter
    def min_range(self, value: float) -> None:
        self._set_all("min_range", value)
    
    @property
    def reload_time(self) -> float:
        """Attack reload time."""
        t50 = self._get_type50()
        return t50.reload_time if t50 else 0.0
    
    @reload_time.setter
    def reload_time(self, value: float) -> None:
        self._set_all("reload_time", value)
    
    @property
    def accuracy_percent(self) -> int:
        """Attack accuracy percentage (0-100)."""
        t50 = self._get_type50()
        return t50.accuracy_percent if t50 else 0
    
    @accuracy_percent.setter
    def accuracy_percent(self, value: int) -> None:
        self._set_all("accuracy_percent", value)
    
    @property
    def accuracy_dispersion(self) -> float:
        """Attack accuracy dispersion."""
        t50 = self._get_type50()
        return t50.accuracy_dispersion if t50 else 0.0
    
    @accuracy_dispersion.setter
    def accuracy_dispersion(self, value: float) -> None:
        self._set_all("accuracy_dispersion", value)
    
    @property
    def blast_width(self) -> float:
        """Blast/splash damage width."""
        t50 = self._get_type50()
        return t50.blast_width if t50 else 0.0
    
    @blast_width.setter
    def blast_width(self, value: float) -> None:
        self._set_all("blast_width", value)
    
    @property
    def blast_damage(self) -> float:
        """Blast/splash damage amount."""
        t50 = self._get_type50()
        return t50.blast_damage if t50 else 0.0
    
    @blast_damage.setter
    def blast_damage(self, value: float) -> None:
        self._set_all("blast_damage", value)
    
    @property
    def blast_attack_level(self) -> int | UnitClass:
        """Blast attack level."""
        t50 = self._get_type50()
        return t50.blast_attack_level if t50 else 0
    
    @blast_attack_level.setter
    def blast_attack_level(self, value: int | UnitClass) -> None:
        self._set_all("blast_attack_level", value)
    
    @property
    def frame_delay(self) -> int:
        """Frame delay before attack hits."""
        t50 = self._get_type50()
        return t50.frame_delay if t50 else 0
    
    @frame_delay.setter
    def frame_delay(self, value: int) -> None:
        self._set_all("frame_delay", value)
    
    @property
    def break_off_combat(self) -> int:
        """Whether unit can break off combat."""
        t50 = self._get_type50()
        return t50.break_off_combat if t50 else 0
    
    @break_off_combat.setter
    def break_off_combat(self, value: int) -> None:
        self._set_all("break_off_combat", value)
    
    # -------------------------
    # Armor Properties
    # -------------------------
    
    @property
    def base_armor(self) -> int:
        """Base armor value."""
        t50 = self._get_type50()
        return t50.base_armor if t50 else 0
    
    @base_armor.setter
    def base_armor(self, value: int) -> None:
        self._set_all("base_armor", value)
    
    @property
    def defense_terrain_bonus(self) -> int:
        """Terrain defense bonus."""
        t50 = self._get_type50()
        return t50.defense_terrain_bonus if t50 else 0
    
    @defense_terrain_bonus.setter
    def defense_terrain_bonus(self, value: int) -> None:
        self._set_all("defense_terrain_bonus", value)
    
    @property
    def bonus_damage_resistance(self) -> float:
        """Bonus damage resistance."""
        t50 = self._get_type50()
        return t50.bonus_damage_resistance if t50 else 0.0
    
    @bonus_damage_resistance.setter
    def bonus_damage_resistance(self, value: float) -> None:
        self._set_all("bonus_damage_resistance", value)
    
    @property
    def damage_reflection(self) -> float:
        """Damage reflection amount."""
        t50 = self._get_type50()
        return t50.damage_reflection if t50 else 0.0
    
    @damage_reflection.setter
    def damage_reflection(self, value: float) -> None:
        self._set_all("damage_reflection", value)
    
    @property
    def friendly_fire_damage(self) -> float:
        """Friendly fire damage multiplier."""
        t50 = self._get_type50()
        return t50.friendly_fire_damage if t50 else 0.0
    
    @friendly_fire_damage.setter
    def friendly_fire_damage(self, value: float) -> None:
        self._set_all("friendly_fire_damage", value)
    
    # -------------------------
    # Display Properties
    # -------------------------
    
    @property
    def displayed_attack(self) -> int:
        """Displayed attack value in UI."""
        t50 = self._get_type50()
        return t50.displayed_attack if t50 else 0
    
    @displayed_attack.setter
    def displayed_attack(self, value: int) -> None:
        self._set_all("displayed_attack", value)
    
    @property
    def displayed_melee_armour(self) -> int:
        """Displayed melee armor in UI."""
        t50 = self._get_type50()
        return t50.displayed_melee_armour if t50 else 0
    
    @displayed_melee_armour.setter
    def displayed_melee_armour(self, value: int) -> None:
        self._set_all("displayed_melee_armour", value)
    
    @property
    def displayed_range(self) -> float:
        """Displayed range in UI."""
        t50 = self._get_type50()
        return t50.displayed_range if t50 else 0.0
    
    @displayed_range.setter
    def displayed_range(self, value: float) -> None:
        self._set_all("displayed_range", value)
    
    @property
    def displayed_reload_time(self) -> float:
        """Displayed reload time in UI."""
        t50 = self._get_type50()
        return t50.displayed_reload_time if t50 else 0.0
    
    @displayed_reload_time.setter
    def displayed_reload_time(self, value: float) -> None:
        self._set_all("displayed_reload_time", value)
    
    # -------------------------
    # Projectile Properties
    # -------------------------
    
    @property
    def projectile_unit_id(self) -> int:
        """Projectile unit ID."""
        t50 = self._get_type50()
        return t50.projectile_unit_id if t50 else -1
    
    @projectile_unit_id.setter
    def projectile_unit_id(self, value: int) -> None:
        self._set_all("projectile_unit_id", value)
    
    @property
    def graphic_displacement(self) -> tuple:
        """Graphic displacement (x, y, z)."""
        t50 = self._get_type50()
        return t50.graphic_displacement if t50 else (0.0, 0.0, 0.0)
    
    @graphic_displacement.setter
    def graphic_displacement(self, value: tuple) -> None:
        self._set_all("graphic_displacement", value)
    
    @property
    def interrupt_frame(self) -> int:
        """Interrupt frame for attack animation."""
        t50 = self._get_type50()
        return t50.interrupt_frame if t50 else 0
    
    @interrupt_frame.setter
    def interrupt_frame(self, value: int) -> None:
        self._set_all("interrupt_frame", value)
    
    @property
    def garrison_firepower(self) -> float:
        """Firepower bonus when garrisoned."""
        t50 = self._get_type50()
        return t50.garrison_firepower if t50 else 0.0
    
    @garrison_firepower.setter
    def garrison_firepower(self, value: float) -> None:
        self._set_all("garrison_firepower", value)
    
    # -------------------------
    # Attacks/Armors Lists (read-only for now)
    # -------------------------
    
    @property
    def attacks(self) -> list:
        """List of attack types and amounts."""
        t50 = self._get_type50()
        return list(t50.attacks) if t50 else []
    
    @property
    def armours(self) -> list:
        """List of armor types and amounts."""
        t50 = self._get_type50()
        return list(t50.armours) if t50 else []
