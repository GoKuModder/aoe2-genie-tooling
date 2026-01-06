"""
CreationWrapper - Training/creation attribute wrapper for UnitHandle.

Ported from creatable_OLD.py to work with GenieDatParser.

Provides flat property access to CreationInfo (trainable unit) attributes:
- Training: train_time, train_location_id, button_id
- Charges: max_charge, recharge_rate, charge_event
- Graphics: garrison_graphic_id, spawning_graphic_id, upgrade_graphic_id
- Projectiles: total_projectiles, secondary_projectile_unit_id

Maps to GenieDatParser's CreationInfo structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

if TYPE_CHECKING:
    from sections.civilization.unit import Unit
    from Datasets.attributes import HeroStatus, ChargeType, SpecialAbility
    from Datasets.commands import Effect

__all__ = ["CreationWrapper"]


class CreationWrapper:
    """
    Wrapper for CreationInfo (trainable unit) attributes.

    Provides flat property access to all training/creation stats.
    Changes propagate to all units in the provided list.

    Attributes from GenieDatParser CreationInfo:
        costs, train_locations_new, rear_attack_modifier,
        flank_attack_modifier, creatable_type, hero_mode,
        garrisoned_sprite_id, spawning_sprite_id, upgrading_sprite_id,
        hero_glowing_sprite_id, idle_attack_graphic, max_charge,
        charge_regen_rate, charge_event, charge_type, charge_target,
        charge_projectile_unit, attack_priority, invulnerability_level,
        button_icon_id, button_short_tooltip_str_id, button_extend_tooltip_str_id,
        button_hotkey_action, min_conversion_time_modifier, max_conversion_time_modifier,
        conversion_chance_mod, min_projectiles, max_projectiles,
        projectile_spawning_area_width/length/randomness, secondary_projectile_unit_id,
        special_graphic_id, special_activation, displayed_pierce_armor
    """

    __slots__ = ("_units",)

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_creation_info(self) -> Optional[Any]:
        """Get CreationInfo from first unit."""
        if self._units and hasattr(self._units[0], "creation_info") and self._units[0].creation_info:
            return self._units[0].creation_info
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' creation_info."""
        for unit in self._units:
            if hasattr(unit, "creation_info") and unit.creation_info:
                setattr(unit.creation_info, attr, value)

    # -------------------------
    # Training Properties (via train_locations_new[0])
    # -------------------------

    @property
    def train_time(self) -> int:
        """Training time in seconds."""
        c = self._get_creation_info()
        if c and c.train_locations_new:
            return c.train_locations_new[0].train_time
        return 0

    @train_time.setter
    def train_time(self, value: int) -> None:
        for unit in self._units:
            if unit.creation_info and unit.creation_info.train_locations_new:
                unit.creation_info.train_locations_new[0].train_time = value

    @property
    def train_location_id(self) -> int:
        """Building ID where unit is trained."""
        c = self._get_creation_info()
        if c and c.train_locations_new:
            return c.train_locations_new[0].location_unit_id
        return -1

    @train_location_id.setter
    def train_location_id(self, value: int) -> None:
        for unit in self._units:
            if unit.creation_info and unit.creation_info.train_locations_new:
                unit.creation_info.train_locations_new[0].location_unit_id = value

    @property
    def button_id(self) -> int:
        """Button position in training building."""
        c = self._get_creation_info()
        if c and c.train_locations_new:
            return c.train_locations_new[0].button_id
        return 0

    @button_id.setter
    def button_id(self, value: int) -> None:
        for unit in self._units:
            if unit.creation_info and unit.creation_info.train_locations_new:
                unit.creation_info.train_locations_new[0].button_id = value

    @property
    def hot_key_id(self) -> int:
        """Hotkey ID for training."""
        c = self._get_creation_info()
        if c and c.train_locations_new:
            return c.train_locations_new[0].hotkey_id
        return 0

    @hot_key_id.setter
    def hot_key_id(self, value: int) -> None:
        for unit in self._units:
            if unit.creation_info and unit.creation_info.train_locations_new:
                unit.creation_info.train_locations_new[0].hotkey_id = value

    # -------------------------
    # Lists (Read-Only access references)
    # -------------------------

    @property
    def train_locations(self) -> "TrainLocationsManager":
        """Train locations collection manager."""
        from Actual_Tools_GDP.Units.unit_collections import TrainLocationsManager
        return TrainLocationsManager(self._units)

    @train_locations.setter
    def train_locations(self, value: List) -> None:
        """Set the entire train locations list for all units."""
        for u in self._units:
            if u.creation_info:
                u.creation_info.train_locations_new = value

    @property
    def resource_costs(self) -> "CostsManager":
        """Costs collection manager."""
        from Actual_Tools_GDP.Units.unit_collections import CostsManager
        return CostsManager(self._units)

    @resource_costs.setter
    def resource_costs(self, value: List) -> None:
        """Set the entire costs list for all units."""
        for u in self._units:
            if u.creation_info:
                u.creation_info.costs = value

    @property
    def costs(self) -> "CostsManager":
        """Alias for resource_costs."""
        return self.resource_costs

    # -------------------------
    # Graphics
    # -------------------------

    @property
    def garrison_graphic_id(self) -> int:
        """Garrison graphic ID."""
        c = self._get_creation_info()
        return c.garrisoned_sprite_id if c else -1

    @garrison_graphic_id.setter
    def garrison_graphic_id(self, value: int) -> None:
        self._set_all("garrisoned_sprite_id", value)

    @property
    def spawning_graphic_id(self) -> int:
        """Spawning/creation graphic ID."""
        c = self._get_creation_info()
        return c.spawning_sprite_id if c else -1

    @spawning_graphic_id.setter
    def spawning_graphic_id(self, value: int) -> None:
        self._set_all("spawning_sprite_id", value)

    @property
    def upgrade_graphic_id(self) -> int:
        """Upgrade graphic ID."""
        c = self._get_creation_info()
        return c.upgrading_sprite_id if c else -1

    @upgrade_graphic_id.setter
    def upgrade_graphic_id(self, value: int) -> None:
        self._set_all("upgrading_sprite_id", value)

    @property
    def hero_glow_graphic_id(self) -> int:
        """Hero glow graphic ID."""
        c = self._get_creation_info()
        return c.hero_glowing_sprite_id if c else -1

    @hero_glow_graphic_id.setter
    def hero_glow_graphic_id(self, value: int) -> None:
        self._set_all("hero_glowing_sprite_id", value)

    @property
    def idle_attack_graphic_id(self) -> int:
        """Idle attack graphic ID."""
        c = self._get_creation_info()
        return c.idle_attack_graphic if c else -1

    @idle_attack_graphic_id.setter
    def idle_attack_graphic_id(self, value: int) -> None:
        self._set_all("idle_attack_graphic", value)

    @property
    def special_graphic_id(self) -> int:
        """Special ability graphic ID."""
        c = self._get_creation_info()
        return c.special_graphic_id if c else -1

    @special_graphic_id.setter
    def special_graphic_id(self, value: int) -> None:
        self._set_all("special_graphic_id", value)

    # -------------------------
    # Charge Properties
    # -------------------------

    @property
    def max_charge(self) -> float:
        """Maximum charge amount."""
        c = self._get_creation_info()
        return c.max_charge if c else 0.0

    @max_charge.setter
    def max_charge(self, value: float) -> None:
        self._set_all("max_charge", value)

    @property
    def recharge_rate(self) -> float:
        """Charge recharge rate."""
        c = self._get_creation_info()
        return c.charge_regen_rate if c else 0.0

    @recharge_rate.setter
    def recharge_rate(self, value: float) -> None:
        self._set_all("charge_regen_rate", value)

    @property
    def charge_event(self) -> int:
        """Charge event type."""
        c = self._get_creation_info()
        return c.charge_event if c else 0

    @charge_event.setter
    def charge_event(self, value: int) -> None:
        self._set_all("charge_event", value)

    @property
    def charge_type(self) -> int:
        """Charge type."""
        c = self._get_creation_info()
        return c.charge_type if c else 0

    @charge_type.setter
    def charge_type(self, value: int) -> None:
        self._set_all("charge_type", value)

    @property
    def charge_target(self) -> int:
        """Charge target type."""
        c = self._get_creation_info()
        return c.charge_target if c else 0

    @charge_target.setter
    def charge_target(self, value: int) -> None:
        self._set_all("charge_target", value)

    @property
    def charge_projectile_unit_id(self) -> int:
        """Charge projectile unit ID."""
        c = self._get_creation_info()
        return c.charge_projectile_unit if c else -1

    @charge_projectile_unit_id.setter
    def charge_projectile_unit_id(self, value: int) -> None:
        self._set_all("charge_projectile_unit", value)

    # -------------------------
    # Combat Modifiers
    # -------------------------

    @property
    def rear_attack_modifier(self) -> float:
        """Rear attack damage modifier."""
        c = self._get_creation_info()
        return c.rear_attack_modifier if c else 0.0

    @rear_attack_modifier.setter
    def rear_attack_modifier(self, value: float) -> None:
        self._set_all("rear_attack_modifier", value)

    @property
    def flank_attack_modifier(self) -> float:
        """Flank attack damage modifier."""
        c = self._get_creation_info()
        return c.flank_attack_modifier if c else 0.0

    @flank_attack_modifier.setter
    def flank_attack_modifier(self, value: float) -> None:
        self._set_all("flank_attack_modifier", value)

    @property
    def attack_priority(self) -> int:
        """Attack priority level."""
        c = self._get_creation_info()
        return c.attack_priority if c else 0

    @attack_priority.setter
    def attack_priority(self, value: int) -> None:
        self._set_all("attack_priority", value)

    @property
    def invulnerability_level(self) -> float:
        """Invulnerability level."""
        c = self._get_creation_info()
        return c.invulnerability_level if c else 0.0

    @invulnerability_level.setter
    def invulnerability_level(self, value: float) -> None:
        self._set_all("invulnerability_level", value)

    # -------------------------
    # Conversion Properties
    # -------------------------

    @property
    def min_conversion_time_mod(self) -> float:
        """Minimum conversion time modifier."""
        c = self._get_creation_info()
        return c.min_conversion_time_modifier if c else 0.0

    @min_conversion_time_mod.setter
    def min_conversion_time_mod(self, value: float) -> None:
        self._set_all("min_conversion_time_modifier", value)

    @property
    def max_conversion_time_mod(self) -> float:
        """Maximum conversion time modifier."""
        c = self._get_creation_info()
        return c.max_conversion_time_modifier if c else 0.0

    @max_conversion_time_mod.setter
    def max_conversion_time_mod(self, value: float) -> None:
        self._set_all("max_conversion_time_modifier", value)

    @property
    def conversion_chance_mod(self) -> float:
        """Conversion chance modifier."""
        c = self._get_creation_info()
        return c.conversion_chance_mod if c else 0.0

    @conversion_chance_mod.setter
    def conversion_chance_mod(self, value: float) -> None:
        self._set_all("conversion_chance_mod", value)

    # -------------------------
    # Projectile Properties
    # -------------------------

    @property
    def total_projectiles(self) -> float:
        """Total projectiles per attack (minimum projectiles)."""
        c = self._get_creation_info()
        return c.min_projectiles if c else 0.0

    @total_projectiles.setter
    def total_projectiles(self, value: float) -> None:
        self._set_all("min_projectiles", value)

    @property
    def max_total_projectiles(self) -> int:
        """Maximum total projectiles."""
        c = self._get_creation_info()
        return c.max_projectiles if c else 0

    @max_total_projectiles.setter
    def max_total_projectiles(self, value: int) -> None:
        self._set_all("max_projectiles", value)

    @property
    def secondary_projectile_unit_id(self) -> int:
        """Secondary projectile unit ID."""
        c = self._get_creation_info()
        return c.secondary_projectile_unit_id if c else -1

    @secondary_projectile_unit_id.setter
    def secondary_projectile_unit_id(self, value: int) -> None:
        self._set_all("secondary_projectile_unit_id", value)

    @property
    def projectile_spawning_area(self) -> Tuple[float, float, float]:
        """Projectile spawning area (width, length, randomness)."""
        c = self._get_creation_info()
        if c:
            return (
                c.projectile_spawning_area_width,
                c.projectile_spawning_area_length,
                c.projectile_spawning_area_randomness,
            )
        return (0.0, 0.0, 0.0)

    @projectile_spawning_area.setter
    def projectile_spawning_area(self, value: Tuple[float, float, float]) -> None:
        for unit in self._units:
            if hasattr(unit, "creation_info") and unit.creation_info:
                unit.creation_info.projectile_spawning_area_width = value[0]
                unit.creation_info.projectile_spawning_area_length = value[1]
                unit.creation_info.projectile_spawning_area_randomness = value[2]

    @property
    def projectile_spawning_area_width(self) -> float:
        """Projectile spawning area width."""
        c = self._get_creation_info()
        return c.projectile_spawning_area_width if c else 0.0

    @projectile_spawning_area_width.setter
    def projectile_spawning_area_width(self, value: float) -> None:
        self._set_all("projectile_spawning_area_width", value)

    @property
    def projectile_spawning_area_length(self) -> float:
        """Projectile spawning area length."""
        c = self._get_creation_info()
        return c.projectile_spawning_area_length if c else 0.0

    @projectile_spawning_area_length.setter
    def projectile_spawning_area_length(self, value: float) -> None:
        self._set_all("projectile_spawning_area_length", value)

    @property
    def projectile_spawning_area_randomness(self) -> float:
        """Projectile spawning area randomness."""
        c = self._get_creation_info()
        return c.projectile_spawning_area_randomness if c else 0.0

    @projectile_spawning_area_randomness.setter
    def projectile_spawning_area_randomness(self, value: float) -> None:
        self._set_all("projectile_spawning_area_randomness", value)

    # -------------------------
    # UI/Button Properties
    # -------------------------

    @property
    def button_icon_id(self) -> int:
        """Button icon ID."""
        c = self._get_creation_info()
        return c.button_icon_id if c else 0

    @button_icon_id.setter
    def button_icon_id(self, value: int) -> None:
        self._set_all("button_icon_id", value)

    @property
    def button_short_tooltip_id(self) -> int:
        """Button short tooltip string ID."""
        c = self._get_creation_info()
        return c.button_short_tooltip_str_id if c else 0

    @button_short_tooltip_id.setter
    def button_short_tooltip_id(self, value: int) -> None:
        self._set_all("button_short_tooltip_str_id", value)

    @property
    def button_extended_tooltip_id(self) -> int:
        """Button extended tooltip string ID."""
        c = self._get_creation_info()
        return c.button_extend_tooltip_str_id if c else 0

    @button_extended_tooltip_id.setter
    def button_extended_tooltip_id(self, value: int) -> None:
        self._set_all("button_extend_tooltip_str_id", value)

    @property
    def button_hotkey_action(self) -> int:
        """Button hotkey action ID."""
        c = self._get_creation_info()
        return c.button_hotkey_action if c else 0

    @button_hotkey_action.setter
    def button_hotkey_action(self, value: int) -> None:
        self._set_all("button_hotkey_action", value)

    # -------------------------
    # Misc Properties
    # -------------------------

    @property
    def creatable_type(self) -> int:
        """Creatable type (unit/building)."""
        c = self._get_creation_info()
        return c.creatable_type if c else 0

    @creatable_type.setter
    def creatable_type(self, value: int) -> None:
        self._set_all("creatable_type", value)

    @property
    def hero_mode(self) -> int:
        """Hero mode flag."""
        c = self._get_creation_info()
        return c.hero_mode if c else 0

    @hero_mode.setter
    def hero_mode(self, value: int) -> None:
        self._set_all("hero_mode", value)

    @property
    def special_ability(self) -> int:
        """Special ability type (special_activation)."""
        c = self._get_creation_info()
        return c.special_activation if c else 0

    @special_ability.setter
    def special_ability(self, value: int) -> None:
        self._set_all("special_activation", value)

    @property
    def displayed_pierce_armour(self) -> int:
        """Displayed pierce armor in UI."""
        c = self._get_creation_info()
        return c.displayed_pierce_armor if c else 0

    @displayed_pierce_armour.setter
    def displayed_pierce_armour(self, value: int) -> None:
        self._set_all("displayed_pierce_armor", value)
