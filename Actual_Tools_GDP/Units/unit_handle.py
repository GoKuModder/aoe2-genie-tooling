"""
UnitHandle - High-level wrapper for Genie Unit objects.

Ported from unit_handle_OLD.py to work with GenieDatParser.

Provides full attribute flattening: access any attribute directly on the handle.
    unit.move_sound = 1      # Auto-finds movement_info.move_sound
    unit.attack_graphic = 5  # Auto-finds combat_info.attack_graphic
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

# Import DamageClass for attack/armour creation
from sections.civilization.type_info.damage_class import DamageClass

# Handle imports (ported versions - may need to create these)
from Actual_Tools_GDP.Units.handles import (
    TaskHandle, AttackHandle, ArmourHandle, DamageGraphicHandle,
    TrainLocationHandle, DropSiteHandle
)

from Actual_Tools_GDP.Units.wrappers import (
    CombatWrapper,
    CreationWrapper,
    MovementWrapper,
    BehaviorWrapper,
    ProjectileWrapper, 
    BuildingWrapper
)

# Collection Manager imports
from Actual_Tools_GDP.Units.unit_collections import (
    TasksManager as TasksWrapper,
    AttacksManager,
    ArmoursManager,
    DamageGraphicsManager as DamageGraphicsWrapper,
    TrainLocationsManager as TrainLocationsWrapper,
    DropSitesManager,
    AnnexesManager,
    CostsManager as CostWrapper,
    ResourcesManager as ResourceStoragesWrapper
)

# Validation moved to workspace.py (centralized)

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["UnitHandle"]

# Component names for flattening lookup
_COMPONENTS = ("behavior", "movement", "combat", "projectile", "creation", "building")


class UnitHandle:
    """
    High-level wrapper for Genie Unit objects with full attribute flattening.

    All attributes from Unit, Bird, DeadFish, Type50, Projectile, Creatable,
    and Building are accessible directly on this object.
    
    Validation:
        Setting reference fields (like standing_graphic, attack_sound) validates
        that the referenced ID exists in the workspace.

    Args:
        workspace: The GenieWorkspace reference.
        unit_id: The unit ID to wrap.
        civ_ids: List of civilization IDs to affect. None = all civs.

    Examples:
        >>> unit = workspace.unit_manager.get(4)  # Archer
        >>> unit.hit_points = 100           # Direct Unit attr
        >>> unit.move_sound = 5             # bird.move_sound
        >>> attack = unit.add_attack(class_=4, amount=6)
        >>> print(attack.attack_id)         # Get index
    """

    __slots__ = (
        "_workspace", "_unit_id", "_civ_ids", "_units_cache", 
        # removed "_validator" (using workspace.validator)
        
        # Wrapper caches
        "_combat_cache", "_creation_cache", "_cost_cache", "_movement_cache",
        "_behavior_cache", "_projectile_cache", "_building_cache",
        # Collection caches
        "_tasks_cache", "_attacks_cache", "_armours_cache", 
        "_damage_graphics_cache", "_train_locations_cache", 
        "_annexes_cache", "_drop_sites_cache", "_costs_cache", "_resources_cache",
    )

    def __init__(
        self, 
        workspace: GenieWorkspace, 
        unit_id: int, 
        civ_ids: Optional[List[int]] = None
    ) -> None:
        if unit_id < 0:
            raise ValueError(f"unit_id must be non-negative, got {unit_id}")

        object.__setattr__(self, "_workspace", workspace)
        object.__setattr__(self, "_unit_id", unit_id)
        
        if civ_ids is None:
            civ_ids = list(range(len(workspace.dat.civilizations)))
        object.__setattr__(self, "_civ_ids", civ_ids)
        object.__setattr__(self, "_units_cache", None)
        # _validator init removed
        # Initialize wrapper caches to None
        object.__setattr__(self, "_combat_cache", None)
        object.__setattr__(self, "_creation_cache", None)
        object.__setattr__(self, "_cost_cache", None)
        object.__setattr__(self, "_movement_cache", None)
        object.__setattr__(self, "_behavior_cache", None)
        object.__setattr__(self, "_projectile_cache", None)
        object.__setattr__(self, "_building_cache", None)
        # Collection caches
        object.__setattr__(self, "_tasks_cache", None)
        object.__setattr__(self, "_attacks_cache", None)
        object.__setattr__(self, "_armours_cache", None)
        object.__setattr__(self, "_damage_graphics_cache", None)
        object.__setattr__(self, "_train_locations_cache", None)
        object.__setattr__(self, "_annexes_cache", None)
        object.__setattr__(self, "_drop_sites_cache", None)
        object.__setattr__(self, "_costs_cache", None)
        object.__setattr__(self, "_resources_cache", None)

    def __repr__(self) -> str:
        name = self.name if self._primary_unit else "<no unit>"
        return f"UnitHandle(id={self._unit_id}, name={name!r}, civs={len(self._civ_ids)})"

    # =========================================================================
    # CORE UNIT ACCESS
    # =========================================================================

    def _get_units(self) -> List[Any]:
        """Get all Unit objects for enabled civs. Cached for performance."""
        if self._units_cache is not None:
            return self._units_cache

        civs = self._workspace.dat.civilizations
        units = []
        for civ_id in self._civ_ids:
            if 0 <= civ_id < len(civs):
                civ = civs[civ_id]
                if 0 <= self._unit_id < len(civ.units):
                    unit = civ.units[self._unit_id]
                    if unit is not None:
                        units.append(unit)

        object.__setattr__(self, "_units_cache", units)
        return units

    def invalidate_cache(self) -> None:
        """Clear cached units and wrapper caches. Call after changing civ_ids."""
        object.__setattr__(self, "_units_cache", None)
        # Wrapper caches
        object.__setattr__(self, "_combat_cache", None)
        object.__setattr__(self, "_creation_cache", None)
        object.__setattr__(self, "_cost_cache", None)
        object.__setattr__(self, "_movement_cache", None)
        object.__setattr__(self, "_behavior_cache", None)
        object.__setattr__(self, "_projectile_cache", None)
        object.__setattr__(self, "_building_cache", None)
        # Collection caches
        object.__setattr__(self, "_tasks_cache", None)
        object.__setattr__(self, "_attacks_cache", None)
        object.__setattr__(self, "_armours_cache", None)
        object.__setattr__(self, "_damage_graphics_cache", None)
        object.__setattr__(self, "_train_locations_cache", None)
        object.__setattr__(self, "_annexes_cache", None)
        object.__setattr__(self, "_drop_sites_cache", None)
        object.__setattr__(self, "_costs_cache", None)
        object.__setattr__(self, "_resources_cache", None)

    @property
    def _primary_unit(self) -> Optional[Any]:
        """First unit (used for reading values)."""
        units = self._get_units()
        return units[0] if units else None

    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================

    @property
    def id(self) -> int:
        """Unit ID."""
        return self._unit_id

    @property
    def unit_id(self) -> int:
        """Unit ID (alias for id)."""
        return self._unit_id

    @property
    def name(self) -> str:
        """Unit name."""
        u = self._primary_unit
        return u.name if u else ""

    @name.setter
    def name(self, value: str) -> None:
        for u in self._get_units():
            u.name = value

    # Frequently used Unit attributes
    @property
    def type_(self) -> int:
        """Unit type."""
        u = self._primary_unit
        return u.type_ if u else 0

    @type_.setter
    def type_(self, value: int) -> None:
        for u in self._get_units():
            u.type_ = value

    @property
    def enabled(self) -> int:
        """Whether unit is enabled."""
        u = self._primary_unit
        return u.enabled if u else 0

    @enabled.setter
    def enabled(self, value: int) -> None:
        for u in self._get_units():
            u.enabled = value

    @property
    def disabled(self) -> int:
        """Whether unit is disabled."""
        u = self._primary_unit
        return u.disabled if u else 0

    @disabled.setter
    def disabled(self, value: int) -> None:
        for u in self._get_units():
            u.disabled = value

    @property
    def class_(self) -> int:
        """Unit class."""
        u = self._primary_unit
        return u.class_ if u else 0

    @class_.setter
    def class_(self, value: int) -> None:
        for u in self._get_units():
            u.class_ = value

    @property
    def hit_points(self) -> int:
        """Unit hit points / health."""
        u = self._primary_unit
        return u.hit_points if u else 0

    @hit_points.setter
    def hit_points(self, value: int) -> None:
        for u in self._get_units():
            u.hit_points = value

    @property
    def line_of_sight(self) -> float:
        """Unit line of sight range."""
        u = self._primary_unit
        return u.line_of_sight if u else 0.0

    @line_of_sight.setter
    def line_of_sight(self, value: float) -> None:
        for u in self._get_units():
            u.line_of_sight = value

    @property
    def garrison_capacity(self) -> int:
        """Garrison capacity."""
        u = self._primary_unit
        return u.garrison_capacity if u else 0

    @garrison_capacity.setter
    def garrison_capacity(self, value: int) -> None:
        for u in self._get_units():
            u.garrison_capacity = value

    @property
    def speed(self) -> float:
        """Unit movement speed."""
        u = self._primary_unit
        if u and hasattr(u, 'animation_info') and u.animation_info:
            return u.animation_info.speed
        return 0.0

    @speed.setter
    def speed(self, value: float) -> None:
        for u in self._get_units():
            if hasattr(u, 'animation_info') and u.animation_info:
                u.animation_info.speed = value

    # =========================================================================
    # MAIN UNIT PROPERTIES (IMPORTANT attributes from checklist)
    # =========================================================================
    
    # String IDs
    @property
    def name_str_id(self) -> int:
        """String ID for unit name."""
        u = self._primary_unit
        return u.name_str_id if u else 0

    @name_str_id.setter
    def name_str_id(self, value: int) -> None:
        for u in self._get_units():
            u.name_str_id = value

    @property
    def creation_str_id(self) -> int:
        """String ID for creation/description text."""
        u = self._primary_unit
        return u.creation_str_id if u else 0

    @creation_str_id.setter
    def creation_str_id(self, value: int) -> None:
        for u in self._get_units():
            u.creation_str_id = value

    @property
    def help_str_id(self) -> int:
        """String ID for help text."""
        u = self._primary_unit
        return u.help_str_id if u else 0

    @help_str_id.setter
    def help_str_id(self, value: int) -> None:
        for u in self._get_units():
            u.help_str_id = value

    @property
    def hotkey_text_str_id(self) -> int:
        """String ID for hotkey page/help text."""
        u = self._primary_unit
        return u.hotkey_text_str_id if u else 0

    @hotkey_text_str_id.setter
    def hotkey_text_str_id(self, value: int) -> None:
        for u in self._get_units():
            u.hotkey_text_str_id = value

    @property
    def hotkey_str_id(self) -> int:
        """String ID for hotkey."""
        u = self._primary_unit
        return u.hotkey_str_id if u else 0

    @hotkey_str_id.setter
    def hotkey_str_id(self, value: int) -> None:
        for u in self._get_units():
            u.hotkey_str_id = value

    # Graphics/Sprites
    @property
    def trait(self) -> int:
        """Unit trait."""
        u = self._primary_unit
        return u.trait if u else 0

    @trait.setter
    def trait(self, value: int) -> None:
        for u in self._get_units():
            u.trait = value

    @property
    def trait_piece(self) -> int:
        """Trait piece."""
        u = self._primary_unit
        return u.trait_piece if u else 0

    @trait_piece.setter
    def trait_piece(self, value: int) -> None:
        for u in self._get_units():
            u.trait_piece = value

    @property
    def standing_sprite_id1(self) -> int:
        """Primary standing sprite ID."""
        u = self._primary_unit
        return u.standing_sprite_id1 if u else -1

    @standing_sprite_id1.setter
    def standing_sprite_id1(self, value: int) -> None:
        for u in self._get_units():
            u.standing_sprite_id1 = value

    @property
    def standing_sprite_id2(self) -> int:
        """Secondary standing sprite ID."""
        u = self._primary_unit
        return u.standing_sprite_id2 if u else -1

    @standing_sprite_id2.setter
    def standing_sprite_id2(self, value: int) -> None:
        for u in self._get_units():
            u.standing_sprite_id2 = value

    @property
    def dying_sprite_id(self) -> int:
        """Dying sprite ID."""
        u = self._primary_unit
        return u.dying_sprite_id if u else -1

    @dying_sprite_id.setter
    def dying_sprite_id(self, value: int) -> None:
        for u in self._get_units():
            u.dying_sprite_id = value

    @property
    def undead_sprite_id(self) -> int:
        """Undead sprite ID."""
        u = self._primary_unit
        return u.undead_sprite_id if u else -1

    @undead_sprite_id.setter
    def undead_sprite_id(self, value: int) -> None:
        for u in self._get_units():
            u.undead_sprite_id = value

    @property
    def icon_id(self) -> int:
        """Icon ID."""
        u = self._primary_unit
        return u.icon_id if u else -1

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        for u in self._get_units():
            u.icon_id = value

    # Physical Dimensions
    @property
    def radius_x(self) -> float:
        """X radius."""
        u = self._primary_unit
        return u.radius_x if u else 0

    @radius_x.setter
    def radius_x(self, value: float) -> None:
        for u in self._get_units():
            u.radius_x = value

    @property
    def radius_y(self) -> float:
        """Y radius."""
        u = self._primary_unit
        return u.radius_y if u else 0

    @radius_y.setter
    def radius_y(self, value: float) -> None:
        for u in self._get_units():
            u.radius_y = value

    @property
    def radius_z(self) -> float:
        """Z radius."""
        u = self._primary_unit
        return u.radius_z if u else 0

    @radius_z.setter
    def radius_z(self, value: float) -> None:
        for u in self._get_units():
            u.radius_z = value

    @property
    def selection_radius_x(self) -> float:
        """Selection X radius."""
        u = self._primary_unit
        return u.selection_radius_x if u else 0

    @selection_radius_x.setter
    def selection_radius_x(self, value: float) -> None:
        for u in self._get_units():
            u.selection_radius_x = value

    @property
    def selection_radius_y(self) -> float:
        """Selection Y radius."""
        u = self._primary_unit
        return u.selection_radius_y if u else 0

    @selection_radius_y.setter
    def selection_radius_y(self, value: float) -> None:
        for u in self._get_units():
            u.selection_radius_y = value

    @property
    def selection_radius_z(self) -> float:
        """Selection Z radius."""
        u = self._primary_unit
        return u.selection_radius_z if u else 0

    @selection_radius_z.setter
    def selection_radius_z(self, value: float) -> None:
        for u in self._get_units():
            u.selection_radius_z = value

    @property
    def selection_effect(self) -> int:
        """Selection effect."""
        u = self._primary_unit
        return u.selection_effect if u else 1

    @selection_effect.setter
    def selection_effect(self, value: int) -> None:
        for u in self._get_units():
            u.selection_effect = value

    @property
    def editor_selection_color(self) -> int:
        """Editor selection color."""
        u = self._primary_unit
        return u.editor_selection_color if u else 0

    @editor_selection_color.setter
    def editor_selection_color(self, value: int) -> None:
        for u in self._get_units():
            u.editor_selection_color = value

    # Sounds
    @property
    def train_sound_id(self) -> int:
        """Training sound ID."""
        u = self._primary_unit
        return u.train_sound_id if u else -1

    @train_sound_id.setter
    def train_sound_id(self, value: int) -> None:
        for u in self._get_units():
            u.train_sound_id = value

    @property
    def damage_sound_id1(self) -> int:
        """Damage sound ID."""
        u = self._primary_unit
        return u.damage_sound_id1 if u else -1

    @damage_sound_id1.setter
    def damage_sound_id1(self, value: int) -> None:
        for u in self._get_units():
            u.damage_sound_id1 = value

    @property
    def selection_sound_id(self) -> int:
        """Selection sound ID."""
        u = self._primary_unit
        return u.selection_sound_id if u else -1

    @selection_sound_id.setter
    def selection_sound_id(self, value: int) -> None:
        for u in self._get_units():
            u.selection_sound_id = value

    @property
    def dying_sound_id(self) -> int:
        """Dying sound ID."""
        u = self._primary_unit
        return u.dying_sound_id if u else -1

    @dying_sound_id.setter
    def dying_sound_id(self, value: int) -> None:
        for u in self._get_units():
            u.dying_sound_id = value

    @property
    def wwise_train_sound_id(self) -> int:
        """Wwise training sound ID."""
        u = self._primary_unit
        return u.wwise_train_sound_id if u else 0

    @wwise_train_sound_id.setter
    def wwise_train_sound_id(self, value: int) -> None:
        for u in self._get_units():
            u.wwise_train_sound_id = value

    @property
    def wwise_damage_sound_id(self) -> int:
        """Wwise damage sound ID."""
        u = self._primary_unit
        return u.wwise_damage_sound_id if u else 0

    @wwise_damage_sound_id.setter
    def wwise_damage_sound_id(self, value: int) -> None:
        for u in self._get_units():
            u.wwise_damage_sound_id = value

    @property
    def wwise_selection_sound_id(self) -> int:
        """Wwise selection sound ID."""
        u = self._primary_unit
        return u.wwise_selection_sound_id if u else 0

    @wwise_selection_sound_id.setter
    def wwise_selection_sound_id(self, value: int) -> None:
        for u in self._get_units():
            u.wwise_selection_sound_id = value

    @property
    def wwise_dying_sound_id(self) -> int:
        """Wwise dying sound ID."""
        u = self._primary_unit
        return u.wwise_dying_sound_id if u else 0

    @wwise_dying_sound_id.setter
    def wwise_dying_sound_id(self, value: int) -> None:
        for u in self._get_units():
            u.wwise_dying_sound_id = value

    # Death/Corpse
    @property
    def dead_unit_id(self) -> int:
        """Dead unit ID."""
        u = self._primary_unit
        return u.dead_unit_id if u else -1

    @dead_unit_id.setter
    def dead_unit_id(self, value: int) -> None:
        for u in self._get_units():
            u.dead_unit_id = value

    @property
    def blood_unit_id(self) -> int:
        """Blood unit ID."""
        u = self._primary_unit
        return u.blood_unit_id if u else -1

    @blood_unit_id.setter
    def blood_unit_id(self, value: int) -> None:
        for u in self._get_units():
            u.blood_unit_id = value

    @property
    def undead_mode(self) -> int:
        """Undead mode."""
        u = self._primary_unit
        return u.undead_mode if u else 0

    @undead_mode.setter
    def undead_mode(self, value: int) -> None:
        for u in self._get_units():
            u.undead_mode = value

    # Placement/Terrain
    @property
    def can_be_built_on(self) -> int:
        """Can be built on."""
        u = self._primary_unit
        return u.can_be_built_on if u else 0

    @can_be_built_on.setter
    def can_be_built_on(self, value: int) -> None:
        for u in self._get_units():
            u.can_be_built_on = value

    @property
    def required_side_terrain_id1(self) -> int:
        """Required side terrain ID 1."""
        u = self._primary_unit
        return u.required_side_terrain_id1 if u else -1

    @required_side_terrain_id1.setter
    def required_side_terrain_id1(self, value: int) -> None:
        for u in self._get_units():
            u.required_side_terrain_id1 = value

    @property
    def required_side_terrain_id2(self) -> int:
        """Required side terrain ID 2."""
        u = self._primary_unit
        return u.required_side_terrain_id2 if u else -1

    @required_side_terrain_id2.setter
    def required_side_terrain_id2(self, value: int) -> None:
        for u in self._get_units():
            u.required_side_terrain_id2 = value

    @property
    def required_center_terrain_id1(self) -> int:
        """Required center terrain ID 1."""
        u = self._primary_unit
        return u.required_center_terrain_id1 if u else -1

    @required_center_terrain_id1.setter
    def required_center_terrain_id1(self, value: int) -> None:
        for u in self._get_units():
            u.required_center_terrain_id1 = value

    @property
    def required_center_terrain_id2(self) -> int:
        """Required center terrain ID 2."""
        u = self._primary_unit
        return u.required_center_terrain_id2 if u else -1

    @required_center_terrain_id2.setter
    def required_center_terrain_id2(self, value: int) -> None:
        for u in self._get_units():
            u.required_center_terrain_id2 = value

    @property
    def required_clearance_radius_x(self) -> float:
        """Required clearance X radius."""
        u = self._primary_unit
        return u.required_clearance_radius_x if u else 0

    @required_clearance_radius_x.setter
    def required_clearance_radius_x(self, value: float) -> None:
        for u in self._get_units():
            u.required_clearance_radius_x = value

    @property
    def required_clearance_radius_y(self) -> float:
        """Required clearance Y radius."""
        u = self._primary_unit
        return u.required_clearance_radius_y if u else 0

    @required_clearance_radius_y.setter
    def required_clearance_radius_y(self, value: float) -> None:
        for u in self._get_units():
            u.required_clearance_radius_y = value

    @property
    def elevation_restriction_mode(self) -> int:
        """Elevation restriction mode / hill mode."""
        u = self._primary_unit
        return u.elevation_restriction_mode if u else 0

    @elevation_restriction_mode.setter
    def elevation_restriction_mode(self, value: int) -> None:
        for u in self._get_units():
            u.elevation_restriction_mode = value

    @property
    def terrain_restriction_id(self) -> int:
        """Terrain restriction ID."""
        u = self._primary_unit
        return u.terrain_restriction_id if u else 0

    @terrain_restriction_id.setter
    def terrain_restriction_id(self, value: int) -> None:
        for u in self._get_units():
            u.terrain_restriction_id = value

    @property
    def foundation_terrain_id(self) -> int:
        """Foundation terrain ID."""
        u = self._primary_unit
        return u.foundation_terrain_id if u else 0

    @foundation_terrain_id.setter
    def foundation_terrain_id(self, value: int) -> None:
        for u in self._get_units():
            u.foundation_terrain_id = value

    # Movement/Pathfinding
    @property
    def movement_mode(self) -> int:
        """Movement mode / fly mode."""
        u = self._primary_unit
        return u.movement_mode if u else 0

    @movement_mode.setter
    def movement_mode(self, value: int) -> None:
        for u in self._get_units():
            u.movement_mode = value

    @property
    def obstruction_type(self) -> int:
        """Obstruction type."""
        u = self._primary_unit
        return u.obstruction_type if u else 0

    @obstruction_type.setter
    def obstruction_type(self, value: int) -> None:
        for u in self._get_units():
            u.obstruction_type = value

    @property
    def obstruction_class(self) -> int:
        """Obstruction class / selection shape."""
        u = self._primary_unit
        return u.obstruction_class if u else 0

    @obstruction_class.setter
    def obstruction_class(self, value: int) -> None:
        for u in self._get_units():
            u.obstruction_class = value

    # Resources/Economy
    @property
    def resource_carry_capacity(self) -> int:
        """Resource carry capacity."""
        u = self._primary_unit
        return u.resource_carry_capacity if u else 0

    @resource_carry_capacity.setter
    def resource_carry_capacity(self, value: int) -> None:
        for u in self._get_units():
            u.resource_carry_capacity = value

    @property
    def resource_decay_rate(self) -> float:
        """Resource decay rate."""
        u = self._primary_unit
        return u.resource_decay_rate if u else -1

    @resource_decay_rate.setter
    def resource_decay_rate(self, value: float) -> None:
        for u in self._get_units():
            u.resource_decay_rate = value

    @property
    def resource_gather_group(self) -> int:
        """Resource gather group."""
        u = self._primary_unit
        return u.resource_gather_group if u else 0

    @resource_gather_group.setter
    def resource_gather_group(self, value: int) -> None:
        for u in self._get_units():
            u.resource_gather_group = value

    @property
    def enable_auto_gather(self) -> int:
        """Enable auto gather."""
        u = self._primary_unit
        return u.enable_auto_gather if u else 0

    @enable_auto_gather.setter
    def enable_auto_gather(self, value: int) -> None:
        for u in self._get_units():
            u.enable_auto_gather = value

    # Combat/Interaction
    @property
    def blast_defense_level(self) -> int:
        """Blast defense level."""
        u = self._primary_unit
        return u.blast_defense_level if u else 3

    @blast_defense_level.setter
    def blast_defense_level(self, value: int) -> None:
        for u in self._get_units():
            u.blast_defense_level = value

    @property
    def combat_level(self) -> int:
        """Combat level."""
        u = self._primary_unit
        return u.combat_level if u else 0

    @combat_level.setter
    def combat_level(self, value: int) -> None:
        for u in self._get_units():
            u.combat_level = value

    @property
    def old_attack_mode(self) -> int:
        """Old attack mode."""
        u = self._primary_unit
        return u.old_attack_mode if u else 0

    @old_attack_mode.setter
    def old_attack_mode(self, value: int) -> None:
        for u in self._get_units():
            u.old_attack_mode = value

    # Display/Interface
    @property
    def interaction_mode(self) -> int:
        """Interaction mode / select level."""
        u = self._primary_unit
        return u.interaction_mode if u else 0

    @interaction_mode.setter
    def interaction_mode(self, value: int) -> None:
        for u in self._get_units():
            u.interaction_mode = value

    @property
    def minimap_mode(self) -> int:
        """Minimap mode / map draw level."""
        u = self._primary_unit
        return u.minimap_mode if u else 0

    @minimap_mode.setter
    def minimap_mode(self, value: int) -> None:
        for u in self._get_units():
            u.minimap_mode = value

    @property
    def interface_mode(self) -> int:
        """Interface mode / unit level."""
        u = self._primary_unit
        return u.interface_mode if u else 0

    @interface_mode.setter
    def interface_mode(self, value: int) -> None:
        for u in self._get_units():
            u.interface_mode = value

    @property
    def minimap_color(self) -> int:
        """Minimap color."""
        u = self._primary_unit
        return u.minimap_color if u else 0

    @minimap_color.setter
    def minimap_color(self, value: int) -> None:
        for u in self._get_units():
            u.minimap_color = value

    @property
    def fog_visibility_mode(self) -> int:
        """Fog visibility mode."""
        u = self._primary_unit
        return u.fog_visibility_mode if u else 0

    @fog_visibility_mode.setter
    def fog_visibility_mode(self, value: int) -> None:
        for u in self._get_units():
            u.fog_visibility_mode = value

    @property
    def occlusion_mode(self) -> int:
        """Occlusion mode."""
        u = self._primary_unit
        return u.occlusion_mode if u else 0

    @occlusion_mode.setter
    def occlusion_mode(self, value: int) -> None:
        for u in self._get_units():
            u.occlusion_mode = value

    # Miscellaneous
    @property
    def sort_number(self) -> int:
        """Sort number."""
        u = self._primary_unit
        return u.sort_number if u else 0

    @sort_number.setter
    def sort_number(self, value: int) -> None:
        for u in self._get_units():
            u.sort_number = value

    @property
    def hide_in_editor(self) -> int:
        """Hide in editor."""
        u = self._primary_unit
        return u.hide_in_editor if u else 0

    @hide_in_editor.setter
    def hide_in_editor(self, value: int) -> None:
        for u in self._get_units():
            u.hide_in_editor = value

    @property
    def multiple_attribute_mode(self) -> float:
        """Multiple attribute mode."""
        u = self._primary_unit
        return u.multiple_attribute_mode if u else 0

    @multiple_attribute_mode.setter
    def multiple_attribute_mode(self, value: float) -> None:
        for u in self._get_units():
            u.multiple_attribute_mode = value

    @property
    def recyclable(self) -> int:
        """Recyclable."""
        u = self._primary_unit
        return u.recyclable if u else 0

    @recyclable.setter
    def recyclable(self, value: int) -> None:
        for u in self._get_units():
            u.recyclable = value

    @property
    def doppelganger_mode(self) -> int:
        """Doppelganger mode."""
        u = self._primary_unit
        return u.doppelganger_mode if u else 0

    @doppelganger_mode.setter
    def doppelganger_mode(self, value: int) -> None:
        for u in self._get_units():
            u.doppelganger_mode = value

    @property
    def convert_terrain(self) -> int:
        """Convert terrain."""
        u = self._primary_unit
        return u.convert_terrain if u else 0

    @convert_terrain.setter
    def convert_terrain(self, value: int) -> None:
        for u in self._get_units():
            u.convert_terrain = value

    # =========================================================================
    # WRAPPERS (cached for performance)
    # =========================================================================

    @property
    def combat(self) -> Type50Wrapper:
        """Type50 (combat) wrapper. Cached."""
        if self._combat_cache is None:
            object.__setattr__(self, "_combat_cache", Type50Wrapper(self._get_units()))
        return self._combat_cache



    @property
    def creation(self) -> CreationWrapper:
        """Creation wrapper. Cached."""
        if self._creation_cache is None:
            object.__setattr__(self, "_creation_cache", CreationWrapper(self._get_units()))
        return self._creation_cache

    @property
    def cost(self) -> CostWrapper:
        """Cost wrapper. Cached."""
        if self._cost_cache is None:
            object.__setattr__(self, "_cost_cache", CostWrapper(self._get_units()))
        return self._cost_cache





    @property
    def projectile(self) -> ProjectileWrapper:
        """Projectile wrapper. Cached."""
        if self._projectile_cache is None:
            object.__setattr__(self, "_projectile_cache", ProjectileWrapper(self._get_units()))
        return self._projectile_cache

    @property
    def building(self) -> BuildingWrapper:
        """Building wrapper. Cached."""
        if self._building_cache is None:
            object.__setattr__(self, "_building_cache", BuildingWrapper(self._get_units()))
        return self._building_cache

    @property
    def resource_storages(self) -> ResourceStoragesWrapper:
        """Resource storages wrapper. Cached."""
        return self.resources

    @property
    def damage_graphics(self) -> DamageGraphicsWrapper:
        """Damage graphics wrapper. Cached."""
        if self._damage_graphics_cache is None:
            object.__setattr__(self, "_damage_graphics_cache", DamageGraphicsWrapper(self._get_units()))
        return self._damage_graphics_cache

    @property
    def tasks_wrapper(self) -> TasksWrapper:
        """Alias for tasks wrapper."""
        return self.tasks

    @property
    def tasks(self) -> TasksWrapper:
        """Tasks wrapper. Cached."""
        if self._tasks_cache is None:
            object.__setattr__(self, "_tasks_cache", TasksWrapper(self._get_units()))
        return self._tasks_cache

    @property
    def train_locations_wrapper(self) -> TrainLocationsWrapper:
        """Train locations wrapper for managing where unit can be trained."""
        if self._train_locations_cache is None:
            object.__setattr__(self, "_train_locations_cache", TrainLocationsWrapper(self._get_units()))
        return self._train_locations_cache

    # =========================================================================
    # FLATTENED COLLECTIONS
    # =========================================================================

    @property
    def attacks(self) -> AttacksManager:
        """Combat attacks manager."""
        if self._attacks_cache is None:
            object.__setattr__(self, "_attacks_cache", AttacksManager(self._get_units()))
        return self._attacks_cache

    @attacks.setter
    def attacks(self, value: List[DamageClass]) -> None:
        """Batch set attacks for all units."""
        for u in self._get_units():
            if hasattr(u, "combat_info") and u.combat_info:
                u.combat_info.attacks = list(value)

    @property
    def armours(self) -> ArmoursManager:
        """Combat armours manager."""
        if self._armours_cache is None:
            object.__setattr__(self, "_armours_cache", ArmoursManager(self._get_units()))
        return self._armours_cache

    @armours.setter
    def armours(self, value: List[DamageClass]) -> None:
        """Batch set armours for all units."""
        for u in self._get_units():
            if hasattr(u, "combat_info") and u.combat_info:
                u.combat_info.armors = list(value)

    @property
    def resource_costs(self) -> CostWrapper:
        """Alias for costs."""
        return self.costs

    @resource_costs.setter
    def resource_costs(self, value: Any) -> None:
        """Batch set costs for all units."""
        self.costs = list(value) if isinstance(value, (list, tuple)) else value

    @property
    def costs(self) -> CostWrapper:
        """Creatable resource_costs manager."""
        if self._costs_cache is None:
            object.__setattr__(self, "_costs_cache", CostWrapper(self._get_units()))
        return self._costs_cache

    @costs.setter
    def costs(self, value: Any) -> None:
        """Batch set costs for all units."""
        for u in self._get_units():
            if hasattr(u, "creation_info") and u.creation_info:
                u.creation_info.costs = value

    @property
    def resources(self) -> ResourceStoragesWrapper:
        """Resources manager."""
        if self._resources_cache is None:
            object.__setattr__(self, "_resources_cache", ResourceStoragesWrapper(self._get_units()))
        return self._resources_cache

    @resources.setter
    def resources(self, value: Any) -> None:
        """Batch set resources for all units."""
        for u in self._get_units():
            u.resources = value

    @property
    def train_locations(self) -> TrainLocationsWrapper:
        """Train locations manager."""
        if self._train_locations_cache is None:
            object.__setattr__(self, "_train_locations_cache", TrainLocationsWrapper(self._get_units()))
        return self._train_locations_cache

    @train_locations.setter
    def train_locations(self, value: List) -> None:
        """Batch set train locations for all units."""
        for u in self._get_units():
            if hasattr(u, "creation_info") and u.creation_info:
                u.creation_info.train_locations_new = list(value)

    @property
    def annexes(self) -> AnnexesManager:
        """Building annexes manager."""
        if self._annexes_cache is None:
            object.__setattr__(self, "_annexes_cache", AnnexesManager(self._get_units()))
        return self._annexes_cache

    @annexes.setter
    def annexes(self, value: Any) -> None:
        """Batch set annexes for all units."""
        for u in self._get_units():
            if hasattr(u, "building_info") and u.building_info:
                u.building_info.building_annex = value

    @property
    def looting_table(self) -> Any:
        """Building looting_table."""
        u = self._primary_unit
        if u and hasattr(u, "building_info") and u.building_info:
            return u.building_info.salvage_attributes
        return None

    @looting_table.setter
    def looting_table(self, value: Any) -> None:
        """Batch set looting table for all units."""
        for u in self._get_units():
            if hasattr(u, "building_info") and u.building_info:
                u.building_info.salvage_attributes = value

    @property
    def drop_sites(self) -> DropSitesManager:
        """Drop sites manager."""
        if self._drop_sites_cache is None:
            object.__setattr__(self, "_drop_sites_cache", DropSitesManager(self._get_units()))
        return self._drop_sites_cache

    @drop_sites.setter
    def drop_sites(self, value: List[int]) -> None:
        """Batch set drop sites for all units."""
        for u in self._get_units():
            if hasattr(u, "task_info") and u.task_info:
                u.task_info.drop_site_unit_ids = list(value)

    # =========================================================================
    # RESOURCE STORAGE METHODS
    # =========================================================================

    def resource_1(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None:
        """Set resource storage slot 1."""
        self.resource_storages.resource_1(type, amount, flag)

    def resource_2(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None:
        """Set resource storage slot 2."""
        self.resource_storages.resource_2(type, amount, flag)

    def resource_3(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None:
        """Set resource storage slot 3."""
        self.resource_storages.resource_3(type, amount, flag)

    # =========================================================================
    # ATTACK METHODS (with handles)
    # =========================================================================

    def add_attack(self, class_: int, amount: int) -> Optional[AttackHandle]:
        """Add attack entry to all units. Returns handle for primary unit's attack."""
        return self.attacks.add(class_, amount)

    def get_attack_by_id(self, attack_id: int) -> Optional[AttackHandle]:
        """Get attack by index."""
        try:
            return self.attacks[attack_id]
        except IndexError:
            return None

    def get_attack_by_class(self, class_: int) -> Optional[AttackHandle]:
        """Get attack by class."""
        return self.attacks.get_by_class(class_)

    def remove_attack(self, attack_id: int) -> bool:
        """Remove attack by index from all units."""
        return self.attacks.remove(attack_id)

    def remove_all_attacks(self) -> None:
        """Remove all attacks from this unit."""
        self.attacks.clear()

    def set_attack(self, class_: int, amount: int) -> Optional[AttackHandle]:
        """Set attack for class (update existing or add new). Returns handle."""
        return self.attacks.set(class_, amount)

    # =========================================================================
    # ARMOUR METHODS (with handles)
    # =========================================================================

    def add_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]:
        """Add armour entry to all units. Returns handle for primary unit's armour."""
        return self.armours.add(class_, amount)

    def get_armour_by_id(self, armour_id: int) -> Optional[ArmourHandle]:
        """Get armour by index."""
        try:
            return self.armours[armour_id]
        except IndexError:
            return None

    def get_armour_by_class(self, class_: int) -> Optional[ArmourHandle]:
        """Get armour by class."""
        return self.armours.get_by_class(class_)

    def remove_armour(self, armour_id: int) -> bool:
        """Remove armour by index from all units."""
        return self.armours.remove(armour_id)

    def set_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]:
        """Set armour for class (update existing or add new). Returns handle."""
        return self.armours.set(class_, amount)

    # =========================================================================
    # DAMAGE GRAPHIC METHODS (with handles)
    # =========================================================================

    def add_damage_graphic(self, graphic_id: int, damage_percent: int, apply_mode: int = 0) -> Optional[DamageGraphicHandle]:
        """Add damage graphic to all units. Returns handle."""
        return self.damage_graphics.add(graphic_id, damage_percent, apply_mode)

    def get_damage_graphic(self, damage_graphic_id: int) -> Optional[DamageGraphicHandle]:
        """Get damage graphic by index."""
        try:
            return self.damage_graphics[damage_graphic_id]
        except IndexError:
            return None

    def remove_damage_graphic(self, damage_graphic_id: int) -> bool:
        """Remove damage graphic by index from all units."""
        return self.damage_graphics.remove(damage_graphic_id)

    # =========================================================================
    # TASK METHODS (with handles)
    # =========================================================================

    @property
    def add_task(self):
        """
        Fluent API for adding typed tasks.
        
        Usage:
            unit.add_task.combat(class_id=0)
            unit.add_task.garrison(class_id=11)
            unit.add_task.aura(work_value_1=10, work_range=5)
        
        Returns:
            TaskBuilder with typed methods for all task types
        """
        from Actual_Tools_GDP.Units.task_builder import TaskBuilder
        return TaskBuilder(self)

    def create_task(
        self,
        task_type: int = 0,
        id: int = 0,
        is_default: int = 0,
        action_type: int = 0,
        class_id: int = -1,
        unit_id: int = -1,
        terrain_id: int = -1,
        resource_in: int = -1,
        resource_out: int = -1,
        work_value_1: float = 0.0,
        work_value_2: float = 0.0,
        work_range: float = 0.0,
        enabled: int = 1,
        **kwargs
    ) -> Optional[TaskHandle]:
        """
        Add task to all units with raw parameters. Returns handle for primary unit's task.
        
        For typed task creation, use add_task property instead:
            unit.add_task.combat()
            unit.add_task.garrison()
        """
        return self.tasks.add(
            task_type=task_type,
            id=id,
            is_default=is_default,
            action_type=action_type,
            class_id=class_id,
            unit_id=unit_id,
            terrain_id=terrain_id,
            resource_in=resource_in,
            resource_out=resource_out,
            work_value_1=work_value_1,
            work_value_2=work_value_2,
            work_range=work_range,
            enabled=enabled,
            **kwargs
        )

    def get_task(self, task_id: int) -> Optional[TaskHandle]:
        """Get task by index."""
        try:
            return self.tasks[task_id]
        except IndexError:
            return None

    def get_tasks_list(self) -> List[TaskHandle]:
        """Get all tasks as handles."""
        return list(self.tasks)

    def remove_task(self, task_id: int) -> bool:
        """Remove task by index from all units."""
        return self.tasks.remove(task_id)

    # =========================================================================
    # TRAIN LOCATION METHODS (with handles)
    # =========================================================================

    def add_train_location(
        self,
        unit_id: int,
        train_time: int = 0,
        button_id: int = 0,
        hot_key_id: int = 0,
    ) -> Optional[TrainLocationHandle]:
        """Add train location to all units. Returns handle."""
        return self.train_locations.add(unit_id, train_time, button_id, hot_key_id)

    def get_train_location(self, train_location_id: int) -> Optional[TrainLocationHandle]:
        """Get train location by index."""
        try:
            return self.train_locations[train_location_id]
        except IndexError:
            return None

    def remove_train_location(self, train_location_id: int) -> bool:
        """Remove train location by index from all units."""
        return self.train_locations.remove(train_location_id)

    # =========================================================================
    # DROP SITE METHODS (with handles)
    # =========================================================================

    def add_drop_site(self, unit_id: int) -> Optional[DropSiteHandle]:
        """Add drop site to all units. Returns handle."""
        return self.drop_sites.add(unit_id)

    def get_drop_site(self, drop_site_id: int) -> Optional[DropSiteHandle]:
        """Get drop site by index."""
        try:
            return self.drop_sites[drop_site_id]
        except IndexError:
            return None

    def remove_drop_site(self, drop_site_id: int) -> bool:
        """Remove drop site by index from all units."""
        return self.drop_sites.remove(drop_site_id)

    # =========================================================================
    # DYNAMIC ATTRIBUTE FLATTENING
    # =========================================================================

    def _find_component(self, name: str) -> Optional[str]:
        """Find which component has the given attribute."""
        # Use wrappers instead of raw unit struct
        for comp in _COMPONENTS:
            # Get wrapper instance (e.g. self.bird)
            if not hasattr(self, comp): continue
            wrapper = getattr(self, comp)
            
            # Check if wrapper has the attribute
            if wrapper is not None and hasattr(wrapper, name):
                return comp
        return None

# =========================================================================

    # =========================================================================
    # MISSING WRAPPER ACCESSORS (Option 1 Requirement)
    # =========================================================================

    @property
    def behavior(self) -> BehaviorWrapper:
        if self._behavior_cache is None:
            self._behavior_cache = BehaviorWrapper(self._get_units())
        return self._behavior_cache

    @property
    def movement(self) -> MovementWrapper:
        if self._movement_cache is None:
            self._movement_cache = MovementWrapper(self._get_units())
        return self._movement_cache

    @property
    def projectile(self) -> ProjectileWrapper:
        if self._projectile_cache is None:
            self._projectile_cache = ProjectileWrapper(self._get_units())
        return self._projectile_cache

    @property
    def creation(self) -> CreationWrapper:
        if self._creation_cache is None:
            self._creation_cache = CreationWrapper(self._get_units())
        return self._creation_cache

    @property
    def building(self) -> BuildingWrapper:
        if self._building_cache is None:
            self._building_cache = BuildingWrapper(self._get_units())
        return self._building_cache
    
    # Combat accessor appears to exist, but ensured here if needed
    @property
    def combat(self) -> CombatWrapper:
        if self._combat_cache is None:
            self._combat_cache = CombatWrapper(self._get_units())
        return self._combat_cache


    # FLATTENED WRAPPER PROPERTIES (Generated by generate_wrapper_properties.py)
# =========================================================================

    # CombatWrapper flattened properties
    @property
    def accuracy_dispersion(self) -> Any:
        """Flattens combat.accuracy_dispersion."""
        return self.combat.accuracy_dispersion

    @accuracy_dispersion.setter
    def accuracy_dispersion(self, value: Any) -> None:
        self.combat.accuracy_dispersion = value

    @property
    def accuracy_percent(self) -> Any:
        """Flattens combat.accuracy_percent."""
        return self.combat.accuracy_percent

    @accuracy_percent.setter
    def accuracy_percent(self, value: Any) -> None:
        self.combat.accuracy_percent = value

    @property
    def armours(self) -> Any:
        """Flattens combat.armours."""
        return self.combat.armours

    @armours.setter
    def armours(self, value: Any) -> None:
        self.combat.armours = value

    @property
    def attack_graphic_2_id(self) -> Any:
        """Flattens combat.attack_graphic_2_id."""
        return self.combat.attack_graphic_2_id

    @attack_graphic_2_id.setter
    def attack_graphic_2_id(self, value: Any) -> None:
        self.combat.attack_graphic_2_id = value

    @property
    def attack_graphic_id(self) -> Any:
        """Flattens combat.attack_graphic_id."""
        return self.combat.attack_graphic_id

    @attack_graphic_id.setter
    def attack_graphic_id(self, value: Any) -> None:
        self.combat.attack_graphic_id = value

    @property
    def attacks(self) -> Any:
        """Flattens combat.attacks."""
        return self.combat.attacks

    @attacks.setter
    def attacks(self, value: Any) -> None:
        self.combat.attacks = value

    @property
    def base_armor(self) -> Any:
        """Flattens combat.base_armor."""
        return self.combat.base_armor

    @base_armor.setter
    def base_armor(self, value: Any) -> None:
        self.combat.base_armor = value

    @property
    def blast_attack_level(self) -> Any:
        """Flattens combat.blast_attack_level."""
        return self.combat.blast_attack_level

    @blast_attack_level.setter
    def blast_attack_level(self, value: Any) -> None:
        self.combat.blast_attack_level = value

    @property
    def blast_damage(self) -> Any:
        """Flattens combat.blast_damage."""
        return self.combat.blast_damage

    @blast_damage.setter
    def blast_damage(self, value: Any) -> None:
        self.combat.blast_damage = value

    @property
    def blast_width(self) -> Any:
        """Flattens combat.blast_width."""
        return self.combat.blast_width

    @blast_width.setter
    def blast_width(self, value: Any) -> None:
        self.combat.blast_width = value

    @property
    def bonus_damage_resistance(self) -> Any:
        """Flattens combat.bonus_damage_resistance."""
        return self.combat.bonus_damage_resistance

    @bonus_damage_resistance.setter
    def bonus_damage_resistance(self, value: Any) -> None:
        self.combat.bonus_damage_resistance = value

    @property
    def break_off_combat(self) -> Any:
        """Flattens combat.break_off_combat."""
        return self.combat.break_off_combat

    @break_off_combat.setter
    def break_off_combat(self, value: Any) -> None:
        self.combat.break_off_combat = value

    @property
    def damage_reflection(self) -> Any:
        """Flattens combat.damage_reflection."""
        return self.combat.damage_reflection

    @damage_reflection.setter
    def damage_reflection(self, value: Any) -> None:
        self.combat.damage_reflection = value

    @property
    def defense_terrain_bonus(self) -> Any:
        """Flattens combat.defense_terrain_bonus."""
        return self.combat.defense_terrain_bonus

    @defense_terrain_bonus.setter
    def defense_terrain_bonus(self, value: Any) -> None:
        self.combat.defense_terrain_bonus = value

    @property
    def displayed_attack(self) -> Any:
        """Flattens combat.displayed_attack."""
        return self.combat.displayed_attack

    @displayed_attack.setter
    def displayed_attack(self, value: Any) -> None:
        self.combat.displayed_attack = value

    @property
    def displayed_melee_armour(self) -> Any:
        """Flattens combat.displayed_melee_armour."""
        return self.combat.displayed_melee_armour

    @displayed_melee_armour.setter
    def displayed_melee_armour(self, value: Any) -> None:
        self.combat.displayed_melee_armour = value

    @property
    def displayed_range(self) -> Any:
        """Flattens combat.displayed_range."""
        return self.combat.displayed_range

    @displayed_range.setter
    def displayed_range(self, value: Any) -> None:
        self.combat.displayed_range = value

    @property
    def displayed_reload_time(self) -> Any:
        """Flattens combat.displayed_reload_time."""
        return self.combat.displayed_reload_time

    @displayed_reload_time.setter
    def displayed_reload_time(self, value: Any) -> None:
        self.combat.displayed_reload_time = value

    @property
    def frame_delay(self) -> Any:
        """Flattens combat.frame_delay."""
        return self.combat.frame_delay

    @frame_delay.setter
    def frame_delay(self, value: Any) -> None:
        self.combat.frame_delay = value

    @property
    def friendly_fire_damage(self) -> Any:
        """Flattens combat.friendly_fire_damage."""
        return self.combat.friendly_fire_damage

    @friendly_fire_damage.setter
    def friendly_fire_damage(self, value: Any) -> None:
        self.combat.friendly_fire_damage = value

    @property
    def garrison_firepower(self) -> Any:
        """Flattens combat.garrison_firepower."""
        return self.combat.garrison_firepower

    @garrison_firepower.setter
    def garrison_firepower(self, value: Any) -> None:
        self.combat.garrison_firepower = value

    @property
    def graphic_displacement(self) -> Any:
        """Flattens combat.graphic_displacement."""
        return self.combat.graphic_displacement

    @graphic_displacement.setter
    def graphic_displacement(self, value: Any) -> None:
        self.combat.graphic_displacement = value

    @property
    def interrupt_frame(self) -> Any:
        """Flattens combat.interrupt_frame."""
        return self.combat.interrupt_frame

    @interrupt_frame.setter
    def interrupt_frame(self, value: Any) -> None:
        self.combat.interrupt_frame = value

    @property
    def max_range(self) -> Any:
        """Flattens combat.max_range."""
        return self.combat.max_range

    @max_range.setter
    def max_range(self, value: Any) -> None:
        self.combat.max_range = value

    @property
    def min_range(self) -> Any:
        """Flattens combat.min_range."""
        return self.combat.min_range

    @min_range.setter
    def min_range(self, value: Any) -> None:
        self.combat.min_range = value

    @property
    def projectile_unit_id(self) -> Any:
        """Flattens combat.projectile_unit_id."""
        return self.combat.projectile_unit_id

    @projectile_unit_id.setter
    def projectile_unit_id(self, value: Any) -> None:
        self.combat.projectile_unit_id = value

    @property
    def reload_time(self) -> Any:
        """Flattens combat.reload_time."""
        return self.combat.reload_time

    @reload_time.setter
    def reload_time(self, value: Any) -> None:
        self.combat.reload_time = value

    @property
    def weapon_offset_x(self) -> Any:
        """Flattens combat.weapon_offset_x."""
        return self.combat.weapon_offset_x

    @weapon_offset_x.setter
    def weapon_offset_x(self, value: Any) -> None:
        self.combat.weapon_offset_x = value

    @property
    def weapon_offset_y(self) -> Any:
        """Flattens combat.weapon_offset_y."""
        return self.combat.weapon_offset_y

    @weapon_offset_y.setter
    def weapon_offset_y(self, value: Any) -> None:
        self.combat.weapon_offset_y = value

    @property
    def weapon_offset_z(self) -> Any:
        """Flattens combat.weapon_offset_z."""
        return self.combat.weapon_offset_z

    @weapon_offset_z.setter
    def weapon_offset_z(self, value: Any) -> None:
        self.combat.weapon_offset_z = value


    # MovementWrapper flattened properties
    @property
    def max_yaw_per_sec_standing(self) -> Any:
        """Flattens movement.max_yaw_per_sec_standing."""
        return self.movement.max_yaw_per_sec_standing

    @max_yaw_per_sec_standing.setter
    def max_yaw_per_sec_standing(self, value: Any) -> None:
        self.movement.max_yaw_per_sec_standing = value

    @property
    def max_yaw_per_sec_walking(self) -> Any:
        """Flattens movement.max_yaw_per_sec_walking."""
        return self.movement.max_yaw_per_sec_walking

    @max_yaw_per_sec_walking.setter
    def max_yaw_per_sec_walking(self, value: Any) -> None:
        self.movement.max_yaw_per_sec_walking = value

    @property
    def max_yaw_per_second_moving(self) -> Any:
        """Flattens movement.max_yaw_per_second_moving."""
        return self.movement.max_yaw_per_second_moving

    @max_yaw_per_second_moving.setter
    def max_yaw_per_second_moving(self, value: Any) -> None:
        self.movement.max_yaw_per_second_moving = value

    @property
    def max_yaw_per_second_stationary(self) -> Any:
        """Flattens movement.max_yaw_per_second_stationary."""
        return self.movement.max_yaw_per_second_stationary

    @max_yaw_per_second_stationary.setter
    def max_yaw_per_second_stationary(self, value: Any) -> None:
        self.movement.max_yaw_per_second_stationary = value

    @property
    def min_collision_size_multiplier(self) -> Any:
        """Flattens movement.min_collision_size_multiplier."""
        return self.movement.min_collision_size_multiplier

    @min_collision_size_multiplier.setter
    def min_collision_size_multiplier(self, value: Any) -> None:
        self.movement.min_collision_size_multiplier = value

    @property
    def old_move_algorithm(self) -> Any:
        """Flattens movement.old_move_algorithm."""
        return self.movement.old_move_algorithm

    @old_move_algorithm.setter
    def old_move_algorithm(self, value: Any) -> None:
        self.movement.old_move_algorithm = value

    @property
    def old_size_class(self) -> Any:
        """Flattens movement.old_size_class."""
        return self.movement.old_size_class

    @old_size_class.setter
    def old_size_class(self, value: Any) -> None:
        self.movement.old_size_class = value

    @property
    def rotation_radius(self) -> Any:
        """Flattens movement.rotation_radius."""
        return self.movement.rotation_radius

    @rotation_radius.setter
    def rotation_radius(self, value: Any) -> None:
        self.movement.rotation_radius = value

    @property
    def rotation_radius_speed(self) -> Any:
        """Flattens movement.rotation_radius_speed."""
        return self.movement.rotation_radius_speed

    @rotation_radius_speed.setter
    def rotation_radius_speed(self, value: Any) -> None:
        self.movement.rotation_radius_speed = value

    @property
    def rotation_speed(self) -> Any:
        """Flattens movement.rotation_speed."""
        return self.movement.rotation_speed

    @rotation_speed.setter
    def rotation_speed(self, value: Any) -> None:
        self.movement.rotation_speed = value

    @property
    def running_graphic_id(self) -> Any:
        """Flattens movement.running_graphic_id."""
        return self.movement.running_graphic_id

    @running_graphic_id.setter
    def running_graphic_id(self, value: Any) -> None:
        self.movement.running_graphic_id = value

    @property
    def standing_yaw_revolution_time(self) -> Any:
        """Flattens movement.standing_yaw_revolution_time."""
        return self.movement.standing_yaw_revolution_time

    @standing_yaw_revolution_time.setter
    def standing_yaw_revolution_time(self, value: Any) -> None:
        self.movement.standing_yaw_revolution_time = value

    @property
    def stationary_yaw_revolution_time(self) -> Any:
        """Flattens movement.stationary_yaw_revolution_time."""
        return self.movement.stationary_yaw_revolution_time

    @stationary_yaw_revolution_time.setter
    def stationary_yaw_revolution_time(self, value: Any) -> None:
        self.movement.stationary_yaw_revolution_time = value

    @property
    def tracking_unit_density(self) -> Any:
        """Flattens movement.tracking_unit_density."""
        return self.movement.tracking_unit_density

    @tracking_unit_density.setter
    def tracking_unit_density(self, value: Any) -> None:
        self.movement.tracking_unit_density = value

    @property
    def tracking_unit_id(self) -> Any:
        """Flattens movement.tracking_unit_id."""
        return self.movement.tracking_unit_id

    @tracking_unit_id.setter
    def tracking_unit_id(self, value: Any) -> None:
        self.movement.tracking_unit_id = value

    @property
    def tracking_unit_mode(self) -> Any:
        """Flattens movement.tracking_unit_mode."""
        return self.movement.tracking_unit_mode

    @tracking_unit_mode.setter
    def tracking_unit_mode(self, value: Any) -> None:
        self.movement.tracking_unit_mode = value

    @property
    def trail_mode(self) -> Any:
        """Flattens movement.trail_mode."""
        return self.movement.trail_mode

    @trail_mode.setter
    def trail_mode(self, value: Any) -> None:
        self.movement.trail_mode = value

    @property
    def trail_spacing(self) -> Any:
        """Flattens movement.trail_spacing."""
        return self.movement.trail_spacing

    @trail_spacing.setter
    def trail_spacing(self, value: Any) -> None:
        self.movement.trail_spacing = value

    @property
    def trailing_unit_id(self) -> Any:
        """Flattens movement.trailing_unit_id."""
        return self.movement.trailing_unit_id

    @trailing_unit_id.setter
    def trailing_unit_id(self, value: Any) -> None:
        self.movement.trailing_unit_id = value

    @property
    def turn_radius(self) -> Any:
        """Flattens movement.turn_radius."""
        return self.movement.turn_radius

    @turn_radius.setter
    def turn_radius(self, value: Any) -> None:
        self.movement.turn_radius = value

    @property
    def turn_radius_speed(self) -> Any:
        """Flattens movement.turn_radius_speed."""
        return self.movement.turn_radius_speed

    @turn_radius_speed.setter
    def turn_radius_speed(self, value: Any) -> None:
        self.movement.turn_radius_speed = value

    @property
    def walking_graphic_id(self) -> Any:
        """Flattens movement.walking_graphic_id."""
        return self.movement.walking_graphic_id

    @walking_graphic_id.setter
    def walking_graphic_id(self, value: Any) -> None:
        self.movement.walking_graphic_id = value


    # BehaviorWrapper flattened properties
    @property
    def attack_sound(self) -> Any:
        """Flattens behavior.attack_sound."""
        return self.behavior.attack_sound

    @attack_sound.setter
    def attack_sound(self, value: Any) -> None:
        self.behavior.attack_sound = value

    @property
    def attack_sound_id(self) -> Any:
        """Flattens behavior.attack_sound_id."""
        return self.behavior.attack_sound_id

    @attack_sound_id.setter
    def attack_sound_id(self, value: Any) -> None:
        self.behavior.attack_sound_id = value

    @property
    def default_task_id(self) -> Any:
        """Flattens behavior.default_task_id."""
        return self.behavior.default_task_id

    @default_task_id.setter
    def default_task_id(self, value: Any) -> None:
        self.behavior.default_task_id = value

    @property
    def drop_site_unit_ids(self) -> Any:
        """Flattens behavior.drop_site_unit_ids."""
        return self.behavior.drop_site_unit_ids

    @drop_site_unit_ids.setter
    def drop_site_unit_ids(self, value: Any) -> None:
        self.behavior.drop_site_unit_ids = value

    @property
    def drop_sites(self) -> Any:
        """Flattens behavior.drop_sites."""
        return self.behavior.drop_sites

    @drop_sites.setter
    def drop_sites(self, value: Any) -> None:
        self.behavior.drop_sites = value

    @property
    def move_sound(self) -> Any:
        """Flattens behavior.move_sound."""
        return self.behavior.move_sound

    @move_sound.setter
    def move_sound(self, value: Any) -> None:
        self.behavior.move_sound = value

    @property
    def move_sound_id(self) -> Any:
        """Flattens behavior.move_sound_id."""
        return self.behavior.move_sound_id

    @move_sound_id.setter
    def move_sound_id(self, value: Any) -> None:
        self.behavior.move_sound_id = value

    @property
    def run_mode(self) -> Any:
        """Flattens behavior.run_mode."""
        return self.behavior.run_mode

    @run_mode.setter
    def run_mode(self, value: Any) -> None:
        self.behavior.run_mode = value

    @property
    def run_pattern(self) -> Any:
        """Flattens behavior.run_pattern."""
        return self.behavior.run_pattern

    @run_pattern.setter
    def run_pattern(self, value: Any) -> None:
        self.behavior.run_pattern = value

    @property
    def search_radius(self) -> Any:
        """Flattens behavior.search_radius."""
        return self.behavior.search_radius

    @search_radius.setter
    def search_radius(self, value: Any) -> None:
        self.behavior.search_radius = value

    @property
    def task_swap_group(self) -> Any:
        """Flattens behavior.task_swap_group."""
        return self.behavior.task_swap_group

    @task_swap_group.setter
    def task_swap_group(self, value: Any) -> None:
        self.behavior.task_swap_group = value

    @property
    def tasks(self) -> Any:
        """Flattens behavior.tasks."""
        return self.behavior.tasks

    @tasks.setter
    def tasks(self, value: Any) -> None:
        self.behavior.tasks = value

    @property
    def work_rate(self) -> Any:
        """Flattens behavior.work_rate."""
        return self.behavior.work_rate

    @work_rate.setter
    def work_rate(self, value: Any) -> None:
        self.behavior.work_rate = value

    @property
    def wwise_attack_sound_id(self) -> Any:
        """Flattens behavior.wwise_attack_sound_id."""
        return self.behavior.wwise_attack_sound_id

    @wwise_attack_sound_id.setter
    def wwise_attack_sound_id(self, value: Any) -> None:
        self.behavior.wwise_attack_sound_id = value

    @property
    def wwise_move_sound_id(self) -> Any:
        """Flattens behavior.wwise_move_sound_id."""
        return self.behavior.wwise_move_sound_id

    @wwise_move_sound_id.setter
    def wwise_move_sound_id(self, value: Any) -> None:
        self.behavior.wwise_move_sound_id = value


    # ProjectileWrapper flattened properties
    @property
    def area_effect_specials(self) -> Any:
        """Flattens projectile.area_effect_specials."""
        return self.projectile.area_effect_specials

    @area_effect_specials.setter
    def area_effect_specials(self, value: Any) -> None:
        self.projectile.area_effect_specials = value

    @property
    def hit_mode(self) -> Any:
        """Flattens projectile.hit_mode."""
        return self.projectile.hit_mode

    @hit_mode.setter
    def hit_mode(self, value: Any) -> None:
        self.projectile.hit_mode = value

    @property
    def projectile_arc(self) -> Any:
        """Flattens projectile.projectile_arc."""
        return self.projectile.projectile_arc

    @projectile_arc.setter
    def projectile_arc(self, value: Any) -> None:
        self.projectile.projectile_arc = value

    @property
    def projectile_type(self) -> Any:
        """Flattens projectile.projectile_type."""
        return self.projectile.projectile_type

    @projectile_type.setter
    def projectile_type(self, value: Any) -> None:
        self.projectile.projectile_type = value

    @property
    def smart_mode(self) -> Any:
        """Flattens projectile.smart_mode."""
        return self.projectile.smart_mode

    @smart_mode.setter
    def smart_mode(self, value: Any) -> None:
        self.projectile.smart_mode = value

    @property
    def vanish_mode(self) -> Any:
        """Flattens projectile.vanish_mode."""
        return self.projectile.vanish_mode

    @vanish_mode.setter
    def vanish_mode(self, value: Any) -> None:
        self.projectile.vanish_mode = value


    # CreationWrapper flattened properties
    @property
    def attack_priority(self) -> Any:
        """Flattens creatable.attack_priority."""
        return self.creatable.attack_priority

    @attack_priority.setter
    def attack_priority(self, value: Any) -> None:
        self.creatable.attack_priority = value

    @property
    def button_extended_tooltip_id(self) -> Any:
        """Flattens creatable.button_extended_tooltip_id."""
        return self.creatable.button_extended_tooltip_id

    @button_extended_tooltip_id.setter
    def button_extended_tooltip_id(self, value: Any) -> None:
        self.creatable.button_extended_tooltip_id = value

    @property
    def button_hotkey_action(self) -> Any:
        """Flattens creatable.button_hotkey_action."""
        return self.creation.button_hotkey_action

    @button_hotkey_action.setter
    def button_hotkey_action(self, value: Any) -> None:
        self.creation.button_hotkey_action = value

    @property
    def button_icon_id(self) -> Any:
        """Flattens creatable.button_icon_id."""
        return self.creation.button_icon_id

    @button_icon_id.setter
    def button_icon_id(self, value: Any) -> None:
        self.creation.button_icon_id = value

    @property
    def button_id(self) -> Any:
        """Flattens creatable.button_id."""
        return self.creation.button_id

    @button_id.setter
    def button_id(self, value: Any) -> None:
        self.creation.button_id = value

    @property
    def button_short_tooltip_id(self) -> Any:
        """Flattens creatable.button_short_tooltip_id."""
        return self.creation.button_short_tooltip_id

    @button_short_tooltip_id.setter
    def button_short_tooltip_id(self, value: Any) -> None:
        self.creation.button_short_tooltip_id = value

    @property
    def charge_event(self) -> Any:
        """Flattens creatable.charge_event."""
        return self.creation.charge_event

    @charge_event.setter
    def charge_event(self, value: Any) -> None:
        self.creation.charge_event = value

    @property
    def charge_projectile_unit_id(self) -> Any:
        """Flattens creatable.charge_projectile_unit_id."""
        return self.creation.charge_projectile_unit_id

    @charge_projectile_unit_id.setter
    def charge_projectile_unit_id(self, value: Any) -> None:
        self.creation.charge_projectile_unit_id = value

    @property
    def charge_target(self) -> Any:
        """Flattens creatable.charge_target."""
        return self.creation.charge_target

    @charge_target.setter
    def charge_target(self, value: Any) -> None:
        self.creation.charge_target = value

    @property
    def charge_type(self) -> Any:
        """Flattens creatable.charge_type."""
        return self.creation.charge_type

    @charge_type.setter
    def charge_type(self, value: Any) -> None:
        self.creation.charge_type = value

    @property
    def conversion_chance_mod(self) -> Any:
        """Flattens creatable.conversion_chance_mod."""
        return self.creation.conversion_chance_mod

    @conversion_chance_mod.setter
    def conversion_chance_mod(self, value: Any) -> None:
        self.creation.conversion_chance_mod = value

    @property
    def costs(self) -> Any:
        """Flattens creatable.costs."""
        return self.creation.costs

    @costs.setter
    def costs(self, value: Any) -> None:
        self.creation.costs = value

    @property
    def creatable_type(self) -> Any:
        """Flattens creatable.creatable_type."""
        return self.creation.creatable_type

    @creatable_type.setter
    def creatable_type(self, value: Any) -> None:
        self.creation.creatable_type = value

    @property
    def displayed_pierce_armour(self) -> Any:
        """Flattens creatable.displayed_pierce_armour."""
        return self.creation.displayed_pierce_armour

    @displayed_pierce_armour.setter
    def displayed_pierce_armour(self, value: Any) -> None:
        self.creation.displayed_pierce_armour = value

    @property
    def flank_attack_modifier(self) -> Any:
        """Flattens creatable.flank_attack_modifier."""
        return self.creation.flank_attack_modifier

    @flank_attack_modifier.setter
    def flank_attack_modifier(self, value: Any) -> None:
        self.creation.flank_attack_modifier = value

    @property
    def garrison_graphic_id(self) -> Any:
        """Flattens creatable.garrison_graphic_id."""
        return self.creation.garrison_graphic_id

    @garrison_graphic_id.setter
    def garrison_graphic_id(self, value: Any) -> None:
        self.creation.garrison_graphic_id = value

    @property
    def hero_glow_graphic_id(self) -> Any:
        """Flattens creatable.hero_glow_graphic_id."""
        return self.creation.hero_glow_graphic_id

    @hero_glow_graphic_id.setter
    def hero_glow_graphic_id(self, value: Any) -> None:
        self.creation.hero_glow_graphic_id = value

    @property
    def hero_mode(self) -> Any:
        """Flattens creatable.hero_mode."""
        return self.creation.hero_mode

    @hero_mode.setter
    def hero_mode(self, value: Any) -> None:
        self.creation.hero_mode = value

    @property
    def hot_key_id(self) -> Any:
        """Flattens creatable.hot_key_id."""
        return self.creation.hot_key_id

    @hot_key_id.setter
    def hot_key_id(self, value: Any) -> None:
        self.creation.hot_key_id = value

    @property
    def idle_attack_graphic_id(self) -> Any:
        """Flattens creatable.idle_attack_graphic_id."""
        return self.creation.idle_attack_graphic_id

    @idle_attack_graphic_id.setter
    def idle_attack_graphic_id(self, value: Any) -> None:
        self.creation.idle_attack_graphic_id = value

    @property
    def invulnerability_level(self) -> Any:
        """Flattens creatable.invulnerability_level."""
        return self.creation.invulnerability_level

    @invulnerability_level.setter
    def invulnerability_level(self, value: Any) -> None:
        self.creation.invulnerability_level = value

    @property
    def max_charge(self) -> Any:
        """Flattens creatable.max_charge."""
        return self.creation.max_charge

    @max_charge.setter
    def max_charge(self, value: Any) -> None:
        self.creation.max_charge = value

    @property
    def max_conversion_time_mod(self) -> Any:
        """Flattens creatable.max_conversion_time_mod."""
        return self.creation.max_conversion_time_mod

    @max_conversion_time_mod.setter
    def max_conversion_time_mod(self, value: Any) -> None:
        self.creation.max_conversion_time_mod = value

    @property
    def max_total_projectiles(self) -> Any:
        """Flattens creatable.max_total_projectiles."""
        return self.creation.max_total_projectiles

    @max_total_projectiles.setter
    def max_total_projectiles(self, value: Any) -> None:
        self.creation.max_total_projectiles = value

    @property
    def min_conversion_time_mod(self) -> Any:
        """Flattens creatable.min_conversion_time_mod."""
        return self.creation.min_conversion_time_mod

    @min_conversion_time_mod.setter
    def min_conversion_time_mod(self, value: Any) -> None:
        self.creation.min_conversion_time_mod = value

    @property
    def projectile_spawning_area(self) -> Any:
        """Flattens creatable.projectile_spawning_area."""
        return self.creation.projectile_spawning_area

    @projectile_spawning_area.setter
    def projectile_spawning_area(self, value: Any) -> None:
        self.creation.projectile_spawning_area = value

    @property
    def projectile_spawning_area_length(self) -> Any:
        """Flattens creatable.projectile_spawning_area_length."""
        return self.creation.projectile_spawning_area_length

    @projectile_spawning_area_length.setter
    def projectile_spawning_area_length(self, value: Any) -> None:
        self.creation.projectile_spawning_area_length = value

    @property
    def projectile_spawning_area_randomness(self) -> Any:
        """Flattens creatable.projectile_spawning_area_randomness."""
        return self.creation.projectile_spawning_area_randomness

    @projectile_spawning_area_randomness.setter
    def projectile_spawning_area_randomness(self, value: Any) -> None:
        self.creation.projectile_spawning_area_randomness = value

    @property
    def projectile_spawning_area_width(self) -> Any:
        """Flattens creatable.projectile_spawning_area_width."""
        return self.creation.projectile_spawning_area_width

    @projectile_spawning_area_width.setter
    def projectile_spawning_area_width(self, value: Any) -> None:
        self.creation.projectile_spawning_area_width = value

    @property
    def rear_attack_modifier(self) -> Any:
        """Flattens creatable.rear_attack_modifier."""
        return self.creation.rear_attack_modifier

    @rear_attack_modifier.setter
    def rear_attack_modifier(self, value: Any) -> None:
        self.creation.rear_attack_modifier = value

    @property
    def recharge_rate(self) -> Any:
        """Flattens creatable.recharge_rate."""
        return self.creation.recharge_rate

    @recharge_rate.setter
    def recharge_rate(self, value: Any) -> None:
        self.creation.recharge_rate = value

    @property
    def resource_costs(self) -> Any:
        """Flattens creatable.resource_costs."""
        return self.creation.resource_costs

    @resource_costs.setter
    def resource_costs(self, value: Any) -> None:
        self.creation.resource_costs = value

    @property
    def secondary_projectile_unit_id(self) -> Any:
        """Flattens creatable.secondary_projectile_unit_id."""
        return self.creation.secondary_projectile_unit_id

    @secondary_projectile_unit_id.setter
    def secondary_projectile_unit_id(self, value: Any) -> None:
        self.creation.secondary_projectile_unit_id = value

    @property
    def spawning_graphic_id(self) -> Any:
        """Flattens creatable.spawning_graphic_id."""
        return self.creation.spawning_graphic_id

    @spawning_graphic_id.setter
    def spawning_graphic_id(self, value: Any) -> None:
        self.creation.spawning_graphic_id = value

    @property
    def special_ability(self) -> Any:
        """Flattens creatable.special_ability."""
        return self.creation.special_ability

    @special_ability.setter
    def special_ability(self, value: Any) -> None:
        self.creation.special_ability = value

    @property
    def special_graphic_id(self) -> Any:
        """Flattens creatable.special_graphic_id."""
        return self.creation.special_graphic_id

    @special_graphic_id.setter
    def special_graphic_id(self, value: Any) -> None:
        self.creation.special_graphic_id = value

    @property
    def total_projectiles(self) -> Any:
        """Flattens creatable.total_projectiles."""
        return self.creation.total_projectiles

    @total_projectiles.setter
    def total_projectiles(self, value: Any) -> None:
        self.creation.total_projectiles = value

    @property
    def train_location_id(self) -> Any:
        """Flattens creatable.train_location_id."""
        return self.creation.train_location_id

    @train_location_id.setter
    def train_location_id(self, value: Any) -> None:
        self.creation.train_location_id = value

    @property
    def train_locations(self) -> Any:
        """Flattens creatable.train_locations."""
        return self.creation.train_locations

    @train_locations.setter
    def train_locations(self, value: Any) -> None:
        self.creation.train_locations = value

    @property
    def train_time(self) -> Any:
        """Flattens creatable.train_time."""
        return self.creation.train_time

    @train_time.setter
    def train_time(self, value: Any) -> None:
        self.creation.train_time = value

    @property
    def upgrade_graphic_id(self) -> Any:
        """Flattens creatable.upgrade_graphic_id."""
        return self.creation.upgrade_graphic_id

    @upgrade_graphic_id.setter
    def upgrade_graphic_id(self, value: Any) -> None:
        self.creation.upgrade_graphic_id = value


    # BuildingWrapper flattened properties
    @property
    def adjacent_mode(self) -> Any:
        """Flattens building.adjacent_mode."""
        return self.building.adjacent_mode

    @adjacent_mode.setter
    def adjacent_mode(self, value: Any) -> None:
        self.building.adjacent_mode = value

    @property
    def annexes(self) -> Any:
        """Flattens building.annexes."""
        return self.building.annexes

    @annexes.setter
    def annexes(self, value: Any) -> None:
        self.building.annexes = value

    @property
    def annexes_manager(self) -> Any:
        """Flattens building.annexes_manager."""
        return self.building.annexes_manager

    @annexes_manager.setter
    def annexes_manager(self, value: Any) -> None:
        self.building.annexes_manager = value

    @property
    def can_burn(self) -> Any:
        """Flattens building.can_burn."""
        return self.building.can_burn

    @can_burn.setter
    def can_burn(self, value: Any) -> None:
        self.building.can_burn = value

    @property
    def completion_tech_id(self) -> Any:
        """Flattens building.completion_tech_id."""
        return self.building.completion_tech_id

    @completion_tech_id.setter
    def completion_tech_id(self, value: Any) -> None:
        self.building.completion_tech_id = value

    @property
    def construction_graphic_id(self) -> Any:
        """Flattens building.construction_graphic_id."""
        return self.building.construction_graphic_id

    @construction_graphic_id.setter
    def construction_graphic_id(self, value: Any) -> None:
        self.building.construction_graphic_id = value

    @property
    def construction_sound_id(self) -> Any:
        """Flattens building.construction_sound_id."""
        return self.building.construction_sound_id

    @construction_sound_id.setter
    def construction_sound_id(self, value: Any) -> None:
        self.building.construction_sound_id = value

    @property
    def destruction_graphic_id(self) -> Any:
        """Flattens building.destruction_graphic_id."""
        return self.building.destruction_graphic_id

    @destruction_graphic_id.setter
    def destruction_graphic_id(self, value: Any) -> None:
        self.building.destruction_graphic_id = value

    @property
    def destruction_rubble_graphic_id(self) -> Any:
        """Flattens building.destruction_rubble_graphic_id."""
        return self.building.destruction_rubble_graphic_id

    @destruction_rubble_graphic_id.setter
    def destruction_rubble_graphic_id(self, value: Any) -> None:
        self.building.destruction_rubble_graphic_id = value

    @property
    def disappears_when_built(self) -> Any:
        """Flattens building.disappears_when_built."""
        return self.building.disappears_when_built

    @disappears_when_built.setter
    def disappears_when_built(self, value: Any) -> None:
        self.building.disappears_when_built = value

    @property
    def foundation_terrain_id(self) -> Any:
        """Flattens building.foundation_terrain_id."""
        return self.building.foundation_terrain_id

    @foundation_terrain_id.setter
    def foundation_terrain_id(self, value: Any) -> None:
        self.building.foundation_terrain_id = value

    @property
    def garrison_heal_rate(self) -> Any:
        """Flattens building.garrison_heal_rate."""
        return self.building.garrison_heal_rate

    @garrison_heal_rate.setter
    def garrison_heal_rate(self, value: Any) -> None:
        self.building.garrison_heal_rate = value

    @property
    def garrison_repair_rate(self) -> Any:
        """Flattens building.garrison_repair_rate."""
        return self.building.garrison_repair_rate

    @garrison_repair_rate.setter
    def garrison_repair_rate(self, value: Any) -> None:
        self.building.garrison_repair_rate = value

    @property
    def garrison_type(self) -> Any:
        """Flattens building.garrison_type."""
        return self.building.garrison_type

    @garrison_type.setter
    def garrison_type(self, value: Any) -> None:
        self.building.garrison_type = value

    @property
    def graphics_angle(self) -> Any:
        """Flattens building.graphics_angle."""
        return self.building.graphics_angle

    @graphics_angle.setter
    def graphics_angle(self, value: Any) -> None:
        self.building.graphics_angle = value

    @property
    def head_unit_id(self) -> Any:
        """Flattens building.head_unit_id."""
        return self.building.head_unit_id

    @head_unit_id.setter
    def head_unit_id(self, value: Any) -> None:
        self.building.head_unit_id = value

    @property
    def looting_table(self) -> Any:
        """Flattens building.looting_table."""
        return self.building.looting_table

    @looting_table.setter
    def looting_table(self, value: Any) -> None:
        self.building.looting_table = value

    @property
    def old_overlap_id(self) -> Any:
        """Flattens building.old_overlap_id."""
        return self.building.old_overlap_id

    @old_overlap_id.setter
    def old_overlap_id(self, value: Any) -> None:
        self.building.old_overlap_id = value

    @property
    def pile_unit_id(self) -> Any:
        """Flattens building.pile_unit_id."""
        return self.building.pile_unit_id

    @pile_unit_id.setter
    def pile_unit_id(self, value: Any) -> None:
        self.building.pile_unit_id = value

    @property
    def research_complete_graphic_id(self) -> Any:
        """Flattens building.research_complete_graphic_id."""
        return self.building.research_complete_graphic_id

    @research_complete_graphic_id.setter
    def research_complete_graphic_id(self, value: Any) -> None:
        self.building.research_complete_graphic_id = value

    @property
    def research_graphic_id(self) -> Any:
        """Flattens building.research_graphic_id."""
        return self.building.research_graphic_id

    @research_graphic_id.setter
    def research_graphic_id(self, value: Any) -> None:
        self.building.research_graphic_id = value

    @property
    def salvage_unit_id(self) -> Any:
        """Flattens building.salvage_unit_id."""
        return self.building.salvage_unit_id

    @salvage_unit_id.setter
    def salvage_unit_id(self, value: Any) -> None:
        self.building.salvage_unit_id = value

    @property
    def snow_graphic_id(self) -> Any:
        """Flattens building.snow_graphic_id."""
        return self.building.snow_graphic_id

    @snow_graphic_id.setter
    def snow_graphic_id(self, value: Any) -> None:
        self.building.snow_graphic_id = value

    @property
    def stack_unit_id(self) -> Any:
        """Flattens building.stack_unit_id."""
        return self.building.stack_unit_id

    @stack_unit_id.setter
    def stack_unit_id(self, value: Any) -> None:
        self.building.stack_unit_id = value

    @property
    def tech_id(self) -> Any:
        """Flattens building.tech_id."""
        return self.building.tech_id

    @tech_id.setter
    def tech_id(self, value: Any) -> None:
        self.building.tech_id = value

    @property
    def transform_sound_id(self) -> Any:
        """Flattens building.transform_sound_id."""
        return self.building.transform_sound_id

    @transform_sound_id.setter
    def transform_sound_id(self, value: Any) -> None:
        self.building.transform_sound_id = value

    @property
    def transform_unit_id(self) -> Any:
        """Flattens building.transform_unit_id."""
        return self.building.transform_unit_id

    @transform_unit_id.setter
    def transform_unit_id(self, value: Any) -> None:
        self.building.transform_unit_id = value

    @property
    def wwise_construction_sound_id(self) -> Any:
        """Flattens building.wwise_construction_sound_id."""
        return self.building.wwise_construction_sound_id

    @wwise_construction_sound_id.setter
    def wwise_construction_sound_id(self, value: Any) -> None:
        self.building.wwise_construction_sound_id = value

    @property
    def wwise_transform_sound_id(self) -> Any:
        """Flattens building.wwise_transform_sound_id."""
        return self.building.wwise_transform_sound_id

    @wwise_transform_sound_id.setter
    def wwise_transform_sound_id(self, value: Any) -> None:
        self.building.wwise_transform_sound_id = value



# =========================================================================
