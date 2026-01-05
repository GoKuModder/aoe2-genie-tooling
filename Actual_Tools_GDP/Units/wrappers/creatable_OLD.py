"""
CreatableWrapper - Training/creation attribute wrapper for UnitHandle.

Provides flat property access to Creatable (trainable unit) attributes:
- Training: train_time, train_location_id, button_id
- Charges: max_charge, recharge_rate, charge_event
- Graphics: garrison_graphic, spawning_graphic, upgrade_graphic
- Projectiles: total_projectiles, secondary_projectile_unit

Mirrors genieutils.unit.Creatable structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    # TODO: Removed genie-rust dependency - needs migration to GenieDatParser
    # from genie_rust import Unit
    pass
    from Datasets.attributes import HeroStatus, ChargeType, SpecialAbility
    from Datasets.commands import Effect

__all__ = ["CreatableWrapper"]


class CreatableWrapper:
    """
    Wrapper for Creatable (trainable unit) attributes.

    Provides flat property access to all training/creation stats.
    Changes propagate to all units in the provided list.

    Attributes from genieutils.unit.Creatable:
        resource_costs, train_locations, rear_attack_modifier,
        flank_attack_modifier, creatable_type, hero_mode,
        garrison_graphic, spawning_graphic, upgrade_graphic,
        hero_glow_graphic, idle_attack_graphic, max_charge,
        recharge_rate, charge_event, charge_type, charge_target,
        charge_projectile_unit, attack_priority, invulnerability_level,
        button_icon_id, button_short_tooltip_id, button_extended_tooltip_id,
        button_hotkey_action, min_conversion_time_mod, max_conversion_time_mod,
        conversion_chance_mod, total_projectiles, max_total_projectiles,
        projectile_spawning_area, secondary_projectile_unit,
        special_graphic, special_ability, displayed_pierce_armour
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_creatable(self) -> Optional[Any]:
        """Get Creatable from first unit."""
        if self._units and hasattr(self._units[0], "creation_info") and self._units[0].creation_info:
            return self._units[0].creation_info
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' creatable."""
        for unit in self._units:
            if hasattr(unit, "creation_info") and unit.creation_info:
                setattr(unit.creation_info, attr, value)

    # -------------------------
    # Training Properties
    # -------------------------

    @property
    def train_time(self) -> int:
        """Training time in seconds."""
        c = self._get_creatable()
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
        c = self._get_creatable()
        if c and c.train_locations_new:
            return c.train_locations_new[0].unit_id
        return -1

    @train_location_id.setter
    def train_location_id(self, value: int) -> None:
        for unit in self._units:
            if unit.creation_info and unit.creation_info.train_locations_new:
                unit.creation_info.train_locations_new[0].unit_id = value

    @property
    def button_id(self) -> int | Effect:
        """Button position in training building."""
        c = self._get_creatable()
        if c and c.train_locations_new:
            return c.train_locations_new[0].button_id
        return 0

    @button_id.setter
    def button_id(self, value: int | Effect) -> None:
        for unit in self._units:
            if unit.creation_info and unit.creation_info.train_locations_new:
                unit.creation_info.train_locations_new[0].button_id = value

    @property
    def hot_key_id(self) -> int:
        """Hotkey ID for training."""
        c = self._get_creatable()
        if c and c.train_locations_new:
            return c.train_locations_new[0].hot_key_id
        return 16000

    @hot_key_id.setter
    def hot_key_id(self, value: int) -> None:
        for unit in self._units:
            if unit.creation_info and unit.creation_info.train_locations_new:
                unit.creation_info.train_locations_new[0].hot_key_id = value

    # -------------------------
    # Lists (Read-Only access references)
    # -------------------------

    @property
    def train_locations(self) -> List:
        """List of TrainLocation objects."""
        c = self._get_creatable()
        return c.train_locations_new if c else []

    @property
    def resource_costs(self) -> Any:
        """List/Tuple of ResourceCost objects."""
        c = self._get_creatable()
        return c.costs if c else []

    # -------------------------
    # Graphics
    # -------------------------

    @property
    def garrison_graphic(self) -> int:
        """Garrison graphic ID."""
        c = self._get_creatable()
        return c.garrisoned_sprite_id if c else -1

    @garrison_graphic.setter
    def garrison_graphic(self, value: int) -> None:
        self._set_all("garrisoned_sprite_id", value)

    @property
    def spawning_graphic(self) -> int:
        """Spawning/creation graphic ID."""
        c = self._get_creatable()
        return c.spawning_sprite_id if c else -1

    @spawning_graphic.setter
    def spawning_graphic(self, value: int) -> None:
        self._set_all("spawning_sprite_id", value)

    @property
    def upgrade_graphic(self) -> int:
        """Upgrade graphic ID."""
        c = self._get_creatable()
        return c.upgrading_sprite_id if c else -1

    @upgrade_graphic.setter
    def upgrade_graphic(self, value: int) -> None:
        self._set_all("upgrading_sprite_id", value)

    @property
    def hero_glow_graphic(self) -> int:
        """Hero glow graphic ID."""
        c = self._get_creatable()
        return c.hero_glowing_sprite_id if c else -1

    @hero_glow_graphic.setter
    def hero_glow_graphic(self, value: int) -> None:
        self._set_all("hero_glowing_sprite_id", value)

    @property
    def idle_attack_graphic(self) -> int:
        """Idle attack graphic ID."""
        c = self._get_creatable()
        return c.idle_attack_graphic if c else -1

    @idle_attack_graphic.setter
    def idle_attack_graphic(self, value: int) -> None:
        self._set_all("idle_attack_graphic", value)

    @property
    def special_graphic(self) -> int:
        """Special ability graphic ID."""
        c = self._get_creatable()
        return c.special_graphic_id if c else -1

    @special_graphic.setter
    def special_graphic(self, value: int) -> None:
        self._set_all("special_graphic_id", value)

    # -------------------------
    # Charge Properties
    # -------------------------

    @property
    def max_charge(self) -> float:
        """Maximum charge amount."""
        c = self._get_creatable()
        return c.max_charge if c else 0.0

    @max_charge.setter
    def max_charge(self, value: float) -> None:
        self._set_all("max_charge", value)

    @property
    def recharge_rate(self) -> float:
        """Charge recharge rate."""
        c = self._get_creatable()
        return c.recharge_rate if c else 0.0

    @recharge_rate.setter
    def recharge_rate(self, value: float) -> None:
        self._set_all("recharge_rate", value)

    @property
    def charge_event(self) -> int:
        """Charge event type."""
        c = self._get_creatable()
        return c.charge_event if c else 0

    @charge_event.setter
    def charge_event(self, value: int) -> None:
        self._set_all("charge_event", value)

    @property
    def charge_type(self) -> int | ChargeType:
        """Charge type."""
        c = self._get_creatable()
        return c.charge_type if c else 0

    @charge_type.setter
    def charge_type(self, value: int | ChargeType) -> None:
        self._set_all("charge_type", value)

    @property
    def charge_target(self) -> int:
        """Charge target type."""
        c = self._get_creatable()
        return c.charge_target if c else 0

    @charge_target.setter
    def charge_target(self, value: int) -> None:
        self._set_all("charge_target", value)

    @property
    def charge_projectile_unit(self) -> int:
        """Charge projectile unit ID."""
        c = self._get_creatable()
        return c.charge_projectile_unit if c else -1

    @charge_projectile_unit.setter
    def charge_projectile_unit(self, value: int) -> None:
        self._set_all("charge_projectile_unit", value)

    # -------------------------
    # Combat Modifiers
    # -------------------------

    @property
    def rear_attack_modifier(self) -> float:
        """Rear attack damage modifier."""
        c = self._get_creatable()
        return c.rear_attack_modifier if c else 0.0

    @rear_attack_modifier.setter
    def rear_attack_modifier(self, value: float) -> None:
        self._set_all("rear_attack_modifier", value)

    @property
    def flank_attack_modifier(self) -> float:
        """Flank attack damage modifier."""
        c = self._get_creatable()
        return c.flank_attack_modifier if c else 0.0

    @flank_attack_modifier.setter
    def flank_attack_modifier(self, value: float) -> None:
        self._set_all("flank_attack_modifier", value)

    @property
    def attack_priority(self) -> int:
        """Attack priority level."""
        c = self._get_creatable()
        return c.attack_priority if c else 0

    @attack_priority.setter
    def attack_priority(self, value: int) -> None:
        self._set_all("attack_priority", value)

    @property
    def invulnerability_level(self) -> float:
        """Invulnerability level."""
        c = self._get_creatable()
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
        c = self._get_creatable()
        return c.min_conversion_time_mod if c else 0.0

    @min_conversion_time_mod.setter
    def min_conversion_time_mod(self, value: float) -> None:
        self._set_all("min_conversion_time_mod", value)

    @property
    def max_conversion_time_mod(self) -> float:
        """Maximum conversion time modifier."""
        c = self._get_creatable()
        return c.max_conversion_time_mod if c else 0.0

    @max_conversion_time_mod.setter
    def max_conversion_time_mod(self, value: float) -> None:
        self._set_all("max_conversion_time_mod", value)

    @property
    def conversion_chance_mod(self) -> float:
        """Conversion chance modifier."""
        c = self._get_creatable()
        return c.conversion_chance_mod if c else 0.0

    @conversion_chance_mod.setter
    def conversion_chance_mod(self, value: float) -> None:
        self._set_all("conversion_chance_mod", value)

    # -------------------------
    # Projectile Properties
    # -------------------------

    @property
    def total_projectiles(self) -> float:
        """Total projectiles per attack."""
        c = self._get_creatable()
        return c.total_projectiles if c else 0.0

    @total_projectiles.setter
    def total_projectiles(self, value: float) -> None:
        self._set_all("total_projectiles", value)

    @property
    def max_total_projectiles(self) -> int:
        """Maximum total projectiles."""
        c = self._get_creatable()
        return c.max_total_projectiles if c else 0

    @max_total_projectiles.setter
    def max_total_projectiles(self, value: int) -> None:
        self._set_all("max_total_projectiles", value)

    @property
    def secondary_projectile_unit(self) -> int:
        """Secondary projectile unit ID."""
        c = self._get_creatable()
        return c.secondary_projectile_unit if c else -1

    @secondary_projectile_unit.setter
    def secondary_projectile_unit(self, value: int) -> None:
        self._set_all("secondary_projectile_unit", value)

    @property
    def projectile_spawning_area(self) -> tuple:
        """Projectile spawning area (x, y, z)."""
        c = self._get_creatable()
        return c.projectile_spawning_area if c else (0.0, 0.0, 0.0)

    @projectile_spawning_area.setter
    def projectile_spawning_area(self, value: tuple) -> None:
        self._set_all("projectile_spawning_area", value)

    # -------------------------
    # UI/Button Properties
    # -------------------------

    @property
    def button_icon_id(self) -> int:
        """Button icon ID."""
        c = self._get_creatable()
        return c.button_icon_id if c else 0

    @button_icon_id.setter
    def button_icon_id(self, value: int) -> None:
        self._set_all("button_icon_id", value)

    @property
    def button_short_tooltip_id(self) -> int:
        """Button short tooltip string ID."""
        c = self._get_creatable()
        return c.button_short_tooltip_id if c else 0

    @button_short_tooltip_id.setter
    def button_short_tooltip_id(self, value: int) -> None:
        self._set_all("button_short_tooltip_id", value)

    @property
    def button_extended_tooltip_id(self) -> int:
        """Button extended tooltip string ID."""
        c = self._get_creatable()
        return c.button_extended_tooltip_id if c else 0

    @button_extended_tooltip_id.setter
    def button_extended_tooltip_id(self, value: int) -> None:
        self._set_all("button_extended_tooltip_id", value)

    @property
    def button_hotkey_action(self) -> int:
        """Button hotkey action ID."""
        c = self._get_creatable()
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
        c = self._get_creatable()
        return c.creatable_type if c else 0

    @creatable_type.setter
    def creatable_type(self, value: int) -> None:
        self._set_all("creatable_type", value)

    @property
    def hero_mode(self) -> int | HeroStatus:
        """Hero mode flag."""
        c = self._get_creatable()
        return c.hero_mode if c else 0

    @hero_mode.setter
    def hero_mode(self, value: int | HeroStatus) -> None:
        self._set_all("hero_mode", value)

    @property
    def special_ability(self) -> int | SpecialAbility:
        """Special ability type."""
        c = self._get_creatable()
        return c.special_ability if c else 0

    @special_ability.setter
    def special_ability(self, value: int | SpecialAbility) -> None:
        self._set_all("special_ability", value)

    @property
    def displayed_pierce_armour(self) -> int:
        """Displayed pierce armor in UI."""
        c = self._get_creatable()
        return c.displayed_pierce_armor if c else 0

    @displayed_pierce_armour.setter
    def displayed_pierce_armour(self, value: int) -> None:
        self._set_all("displayed_pierce_armor", value)
