"""
UnitHandle - High-level wrapper for Genie Unit objects.

Provides full attribute flattening: access any attribute directly on the handle.
    unit.move_sound = 1      # Auto-finds bird.move_sound
    unit.attack_graphic = 5  # Auto-finds type_50.attack_graphic
"""
from __future__ import annotations

import copy
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from genieutils.unit import AttackOrArmor, DamageGraphic, TrainLocation
from genieutils.task import Task

from Actual_Tools.Units.handles import (
    TaskHandle, AttackHandle, ArmourHandle, DamageGraphicHandle,
    TrainLocationHandle, DropSiteHandle
)
from Actual_Tools.Units.wrappers import (
    Type50Wrapper, CreatableWrapper, CostWrapper, DeadFishWrapper,
    BirdWrapper, ProjectileWrapper, BuildingWrapper, ResourceStoragesWrapper,
    DamageGraphicsWrapper, TasksWrapper
)

if TYPE_CHECKING:
    from genieutils.datfile import DatFile
    from genieutils.unit import Unit

__all__ = ["UnitHandle"]

# Component names for flattening lookup
_COMPONENTS = ("bird", "dead_fish", "type_50", "projectile", "creatable", "building")


class UnitHandle:
    """
    High-level wrapper for Genie Unit objects with full attribute flattening.
    
    All attributes from Unit, Bird, DeadFish, Type50, Projectile, Creatable, 
    and Building are accessible directly on this object.
    
    Args:
        unit_id: The unit ID to wrap.
        dat_file: The source DatFile.
        civ_ids: List of civilization IDs to affect. None = all civs.
    
    Examples:
        >>> unit = UnitHandle(4, dat_file)  # Archer
        >>> unit.hit_points = 100           # Direct Unit attr
        >>> unit.move_sound = 5             # bird.move_sound
        >>> attack = unit.add_attack(class_=4, amount=6)
        >>> print(attack.attack_id)         # Get index
    """
    
    __slots__ = ("_unit_id", "_dat_file", "_civ_ids", "_units_cache")
    
    def __init__(self, unit_id: int, dat_file: DatFile, civ_ids: Optional[List[int]] = None) -> None:
        if unit_id < 0:
            raise ValueError(f"unit_id must be non-negative, got {unit_id}")
        
        object.__setattr__(self, "_unit_id", unit_id)
        object.__setattr__(self, "_dat_file", dat_file)
        object.__setattr__(self, "_civ_ids", civ_ids if civ_ids is not None else list(range(len(dat_file.civs))))
        object.__setattr__(self, "_units_cache", None)
    
    def __repr__(self) -> str:
        name = self.name if self._primary_unit else "<no unit>"
        return f"UnitHandle(id={self._unit_id}, name={name!r}, civs={len(self._civ_ids)})"
    
    # =========================================================================
    # CORE UNIT ACCESS
    # =========================================================================
    
    def _get_units(self) -> List[Unit]:
        """Get all Unit objects for enabled civs. Cached for performance."""
        if self._units_cache is not None:
            return self._units_cache
        
        units = []
        for civ_id in self._civ_ids:
            if 0 <= civ_id < len(self._dat_file.civs):
                civ = self._dat_file.civs[civ_id]
                if 0 <= self._unit_id < len(civ.units):
                    unit = civ.units[self._unit_id]
                    if unit is not None:
                        units.append(unit)
        
        object.__setattr__(self, "_units_cache", units)
        return units
    
    def invalidate_cache(self) -> None:
        """Clear cached units. Call after changing civ_ids."""
        object.__setattr__(self, "_units_cache", None)

    @property
    def _primary_unit(self) -> Optional[Unit]:
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
    def name(self) -> str:
        """Unit name."""
        u = self._primary_unit
        return u.name if u else ""
    
    @name.setter
    def name(self, value: str) -> None:
        for u in self._get_units():
            u.name = value

    # =========================================================================
    # WRAPPERS (lazy-initialized via cached_property pattern)
    # =========================================================================
    
    @property
    def combat(self) -> Type50Wrapper:
        """Type50 (combat) wrapper."""
        return Type50Wrapper(self._get_units())
    
    @property
    def creatable(self) -> CreatableWrapper:
        """Creatable wrapper."""
        return CreatableWrapper(self._get_units())
    
    @property
    def cost(self) -> CostWrapper:
        """Cost wrapper."""
        return CostWrapper(self._get_units())
    
    @property
    def dead_fish(self) -> DeadFishWrapper:
        """DeadFish wrapper."""
        return DeadFishWrapper(self._get_units())
    
    @property
    def bird(self) -> BirdWrapper:
        """Bird wrapper."""
        return BirdWrapper(self._get_units())
    
    @property
    def projectile(self) -> ProjectileWrapper:
        """Projectile wrapper."""
        return ProjectileWrapper(self._get_units())
    
    @property
    def building(self) -> BuildingWrapper:
        """Building wrapper."""
        return BuildingWrapper(self._get_units())
    
    @property
    def resource_storages(self) -> ResourceStoragesWrapper:
        """Resource storages wrapper."""
        return ResourceStoragesWrapper(self._get_units())
    
    @property
    def damage_graphics(self) -> DamageGraphicsWrapper:
        """Damage graphics wrapper."""
        return DamageGraphicsWrapper(self._get_units())
    
    @property
    def tasks(self) -> TasksWrapper:
        """Tasks wrapper."""
        return TasksWrapper(self._get_units())
    
    @property
    def train_locations_wrapper(self):
        """Train locations wrapper for managing where unit can be trained."""
        from Actual_Tools.Units.wrappers.train_location import TrainLocationsWrapper
        return TrainLocationsWrapper(self._get_units())


    # =========================================================================
    # FLATTENED COLLECTIONS
    # =========================================================================

    @property
    def attacks(self) -> List[AttackOrArmor]:
        """Type50 attacks list."""
        u = self._primary_unit
        return u.type_50.attacks if u and u.type_50 else []

    @attacks.setter
    def attacks(self, value: List[AttackOrArmor]) -> None:
        for u in self._get_units():
            if u.type_50:
                u.type_50.attacks = value

    @property
    def armours(self) -> List[AttackOrArmor]:
        """Type50 armours list."""
        u = self._primary_unit
        return u.type_50.armours if u and u.type_50 else []

    @armours.setter
    def armours(self, value: List[AttackOrArmor]) -> None:
        for u in self._get_units():
            if u.type_50:
                u.type_50.armours = value

    @property
    def resource_costs(self) -> Tuple:
        """Creatable resource_costs tuple."""
        u = self._primary_unit
        return u.creatable.resource_costs if u and u.creatable else ()

    @resource_costs.setter
    def resource_costs(self, value: Tuple) -> None:
        for u in self._get_units():
            if u.creatable:
                u.creatable.resource_costs = value

    @property
    def train_locations(self) -> List:
        """Creatable train_locations list."""
        u = self._primary_unit
        return u.creatable.train_locations if u and u.creatable else []

    @train_locations.setter
    def train_locations(self, value: List) -> None:
        for u in self._get_units():
            if u.creatable:
                u.creatable.train_locations = value

    @property
    def annexes(self) -> Tuple:
        """Building annexes tuple."""
        u = self._primary_unit
        return u.building.annexes if u and u.building else ()

    @annexes.setter
    def annexes(self, value: Tuple) -> None:
        for u in self._get_units():
            if u.building:
                u.building.annexes = value

    @property
    def looting_table(self) -> Tuple:
        """Building looting_table tuple."""
        u = self._primary_unit
        return u.building.looting_table if u and u.building else ()

    @looting_table.setter
    def looting_table(self, value: Tuple) -> None:
        for u in self._get_units():
            if u.building:
                u.building.looting_table = value

    @property
    def drop_sites(self) -> List[int]:
        """Bird drop_sites list."""
        u = self._primary_unit
        return u.bird.drop_sites if u and u.bird else []

    @drop_sites.setter
    def drop_sites(self, value: List[int]) -> None:
        for u in self._get_units():
            if u.bird:
                u.bird.drop_sites = value

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
        new_attack = AttackOrArmor(class_=class_, amount=amount)
        attack_id = -1
        for u in self._get_units():
            if u.type_50:
                u.type_50.attacks.append(copy.deepcopy(new_attack))
                if attack_id == -1:
                    attack_id = len(u.type_50.attacks) - 1
        
        u = self._primary_unit
        if u and u.type_50 and attack_id >= 0:
            return AttackHandle(u.type_50.attacks[attack_id], attack_id)
        return None

    def get_attack_by_id(self, attack_id: int) -> Optional[AttackHandle]:
        """Get attack by index."""
        u = self._primary_unit
        if u and u.type_50 and 0 <= attack_id < len(u.type_50.attacks):
            return AttackHandle(u.type_50.attacks[attack_id], attack_id)
        return None

    def get_attack_by_class(self, class_: int) -> Optional[AttackHandle]:
        """Get attack by class."""
        u = self._primary_unit
        if u and u.type_50:
            for i, atk in enumerate(u.type_50.attacks):
                if atk.class_ == class_:
                    return AttackHandle(atk, i)
        return None

    def remove_attack(self, attack_id: int) -> bool:
        """Remove attack by index from all units."""
        removed = False
        for u in self._get_units():
            if u.type_50 and 0 <= attack_id < len(u.type_50.attacks):
                u.type_50.attacks.pop(attack_id)
                removed = True
        return removed

    def set_attack(self, class_: int, amount: int) -> Optional[AttackHandle]:
        """Set attack for class (update existing or add new). Returns handle."""
        u = self._primary_unit
        # Check if exists
        if u and u.type_50:
            for i, atk in enumerate(u.type_50.attacks):
                if atk.class_ == class_:
                    # Update all units
                    for unit in self._get_units():
                        if unit.type_50:
                            for a in unit.type_50.attacks:
                                if a.class_ == class_:
                                    a.amount = amount
                                    break
                    return AttackHandle(u.type_50.attacks[i], i)
        # Add new
        return self.add_attack(class_, amount)

    # =========================================================================
    # ARMOUR METHODS (with handles)
    # =========================================================================

    def add_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]:
        """Add armour entry to all units. Returns handle for primary unit's armour."""
        new_armour = AttackOrArmor(class_=class_, amount=amount)
        armour_id = -1
        for u in self._get_units():
            if u.type_50:
                u.type_50.armours.append(copy.deepcopy(new_armour))
                if armour_id == -1:
                    armour_id = len(u.type_50.armours) - 1
        
        u = self._primary_unit
        if u and u.type_50 and armour_id >= 0:
            return ArmourHandle(u.type_50.armours[armour_id], armour_id)
        return None

    def get_armour_by_id(self, armour_id: int) -> Optional[ArmourHandle]:
        """Get armour by index."""
        u = self._primary_unit
        if u and u.type_50 and 0 <= armour_id < len(u.type_50.armours):
            return ArmourHandle(u.type_50.armours[armour_id], armour_id)
        return None

    def get_armour_by_class(self, class_: int) -> Optional[ArmourHandle]:
        """Get armour by class."""
        u = self._primary_unit
        if u and u.type_50:
            for i, arm in enumerate(u.type_50.armours):
                if arm.class_ == class_:
                    return ArmourHandle(arm, i)
        return None

    def remove_armour(self, armour_id: int) -> bool:
        """Remove armour by index from all units."""
        removed = False
        for u in self._get_units():
            if u.type_50 and 0 <= armour_id < len(u.type_50.armours):
                u.type_50.armours.pop(armour_id)
                removed = True
        return removed

    def set_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]:
        """Set armour for class (update existing or add new). Returns handle."""
        u = self._primary_unit
        if u and u.type_50:
            for i, arm in enumerate(u.type_50.armours):
                if arm.class_ == class_:
                    for unit in self._get_units():
                        if unit.type_50:
                            for a in unit.type_50.armours:
                                if a.class_ == class_:
                                    a.amount = amount
                                    break
                    return ArmourHandle(u.type_50.armours[i], i)
        return self.add_armour(class_, amount)

    # =========================================================================
    # DAMAGE GRAPHIC METHODS (with handles)
    # =========================================================================

    def add_damage_graphic(self, graphic_id: int, damage_percent: int, apply_mode: int = 0) -> Optional[DamageGraphicHandle]:
        """Add damage graphic to all units. Returns handle."""
        dmg_id = -1
        for u in self._get_units():
            new_dg = DamageGraphic(graphic_id=graphic_id, damage_percent=damage_percent, apply_mode=apply_mode, old_apply_mode=0)
            u.damage_graphics.append(new_dg)
            if dmg_id == -1:
                dmg_id = len(u.damage_graphics) - 1
        
        u = self._primary_unit
        if u and dmg_id >= 0:
            return DamageGraphicHandle(u.damage_graphics[dmg_id], dmg_id)
        return None

    def get_damage_graphic(self, damage_graphic_id: int) -> Optional[DamageGraphicHandle]:
        """Get damage graphic by index."""
        u = self._primary_unit
        if u and 0 <= damage_graphic_id < len(u.damage_graphics):
            return DamageGraphicHandle(u.damage_graphics[damage_graphic_id], damage_graphic_id)
        return None

    def remove_damage_graphic(self, damage_graphic_id: int) -> bool:
        """Remove damage graphic by index from all units."""
        removed = False
        for u in self._get_units():
            if 0 <= damage_graphic_id < len(u.damage_graphics):
                u.damage_graphics.pop(damage_graphic_id)
                removed = True
        return removed

    # =========================================================================
    # TASK METHODS (with handles)
    # =========================================================================

    def add_task(
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
        """Add task to all units. Returns handle for primary unit's task."""
        task_id = -1
        for u in self._get_units():
            if u.bird:
                new_task = Task(
                    task_type=task_type,
                    id=id,
                    is_default=is_default,
                    action_type=action_type,
                    class_id=class_id,
                    unit_id=unit_id,
                    terrain_id=terrain_id,
                    resource_in=resource_in,
                    resource_out=resource_out,
                    unused_resource=kwargs.get('unused_resource', -1),
                    work_value_1=work_value_1,
                    work_value_2=work_value_2,
                    work_range=work_range,
                    work_flag_2=kwargs.get('work_flag_2', 0),
                    target_diplomacy=kwargs.get('target_diplomacy', 0),
                    carry_check=kwargs.get('carry_check', 0),
                    work_graphic_id=kwargs.get('work_graphic_id', -1),
                    working_graphic_id=kwargs.get('working_graphic_id', -1),
                    carrying_graphic_id=kwargs.get('carrying_graphic_id', -1),
                    resource_gather_sound_id=kwargs.get('resource_gather_sound_id', -1),
                    resource_deposit_sound_id=kwargs.get('resource_deposit_sound_id', -1),
                    wwise_resource_gather_sound_id=kwargs.get('wwise_resource_gather_sound_id', 0),
                    wwise_resource_deposit_sound_id=kwargs.get('wwise_resource_deposit_sound_id', 0),
                    enabled=enabled,
                )
                u.bird.tasks.append(new_task)
                if task_id == -1:
                    task_id = len(u.bird.tasks) - 1
        
        u = self._primary_unit
        if u and u.bird and task_id >= 0:
            return TaskHandle(u.bird.tasks[task_id], task_id)
        return None

    def get_task(self, task_id: int) -> Optional[TaskHandle]:
        """Get task by index."""
        u = self._primary_unit
        if u and u.bird and 0 <= task_id < len(u.bird.tasks):
            return TaskHandle(u.bird.tasks[task_id], task_id)
        return None

    def get_tasks_list(self) -> List[TaskHandle]:
        """Get all tasks as handles."""
        result = []
        u = self._primary_unit
        if u and u.bird:
            for i, task in enumerate(u.bird.tasks):
                result.append(TaskHandle(task, i))
        return result

    def remove_task(self, task_id: int) -> bool:
        """Remove task by index from all units."""
        removed = False
        for u in self._get_units():
            if u.bird and 0 <= task_id < len(u.bird.tasks):
                u.bird.tasks.pop(task_id)
                removed = True
        return removed

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
        loc_id = -1
        for u in self._get_units():
            if u.creatable:
                new_loc = TrainLocation(
                    train_time=train_time,
                    unit_id=unit_id,
                    button_id=button_id,
                    hot_key_id=hot_key_id,
                )
                u.creatable.train_locations.append(new_loc)
                if loc_id == -1:
                    loc_id = len(u.creatable.train_locations) - 1
        
        u = self._primary_unit
        if u and u.creatable and loc_id >= 0:
            return TrainLocationHandle(u.creatable.train_locations[loc_id], loc_id)
        return None

    def get_train_location(self, train_location_id: int) -> Optional[TrainLocationHandle]:
        """Get train location by index."""
        u = self._primary_unit
        if u and u.creatable and 0 <= train_location_id < len(u.creatable.train_locations):
            return TrainLocationHandle(u.creatable.train_locations[train_location_id], train_location_id)
        return None

    def remove_train_location(self, train_location_id: int) -> bool:
        """Remove train location by index from all units."""
        removed = False
        for u in self._get_units():
            if u.creatable and 0 <= train_location_id < len(u.creatable.train_locations):
                u.creatable.train_locations.pop(train_location_id)
                removed = True
        return removed

    # =========================================================================
    # DROP SITE METHODS (with handles)
    # =========================================================================

    def add_drop_site(self, unit_id: int) -> Optional[DropSiteHandle]:
        """Add drop site to all units. Returns handle."""
        site_id = -1
        for u in self._get_units():
            if u.bird:
                u.bird.drop_sites.append(unit_id)
                if site_id == -1:
                    site_id = len(u.bird.drop_sites) - 1
        
        u = self._primary_unit
        if u and u.bird and site_id >= 0:
            return DropSiteHandle(u.bird.drop_sites, site_id)
        return None

    def get_drop_site(self, drop_site_id: int) -> Optional[DropSiteHandle]:
        """Get drop site by index."""
        u = self._primary_unit
        if u and u.bird and 0 <= drop_site_id < len(u.bird.drop_sites):
            return DropSiteHandle(u.bird.drop_sites, drop_site_id)
        return None

    def remove_drop_site(self, drop_site_id: int) -> bool:
        """Remove drop site by index from all units."""
        removed = False
        for u in self._get_units():
            if u.bird and 0 <= drop_site_id < len(u.bird.drop_sites):
                u.bird.drop_sites.pop(drop_site_id)
                removed = True
        return removed

    # =========================================================================
    # DYNAMIC ATTRIBUTE FLATTENING
    # =========================================================================

    def _find_component(self, name: str) -> Optional[str]:
        """Find which component contains the attribute."""
        u = self._primary_unit
        if not u:
            return None
        for comp in _COMPONENTS:
            obj = getattr(u, comp, None)
            if obj is not None and hasattr(obj, name):
                return comp
        return None

    def __getattr__(self, name: str) -> Any:
        u = self._primary_unit
        if not u:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}' (no units)")

        # Direct Unit attribute
        if hasattr(u, name) and name not in _COMPONENTS:
            return getattr(u, name)
        
        # Sub-component attribute
        comp = self._find_component(name)
        if comp:
            return getattr(getattr(u, comp), name)

        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        # Internal slots
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return

        units = self._get_units()
        if not units:
            raise AttributeError(f"Cannot set '{name}': no units linked")

        # Validate and set the value
        self._validated_set(name, value, units)

    def _validated_set(self, name: str, value: Any, units: List) -> None:
        """Set attribute with validation for references and enums."""
        import traceback
        from Actual_Tools_GDP.Shared.manifest_loader import manifest, serializer, DeferredReference
        
        # Get manifest entry for this attribute
        entry = manifest.get_by_name(name)
        
        # Capture source location for error messages
        stack = traceback.extract_stack()
        source_frame = None
        for frame in reversed(stack[:-2]):
            if "site-packages" not in frame.filename and "Actual_Tools" not in frame.filename:
                source_frame = frame
                break
        if source_frame is None:
            source_frame = stack[-3] if len(stack) >= 3 else stack[-1]
        source_info = f"{source_frame.filename}:{source_frame.lineno} - {source_frame.line}"
        
        # VALIDATION: Reference types (deferred to save time)
        if entry and entry.is_reference:
            # Extract ID from value
            actual_id = value
            if not isinstance(value, int):
                if hasattr(value, 'id'):
                    actual_id = value.id
                elif hasattr(value, '_id'):
                    actual_id = value._id
                else:
                    raise TypeError(
                        f"{name}: Expected int or handle object, got {type(value).__name__}\n"
                        f"  Source: {source_info}"
                    )
            
            # Create deferred reference for validation at save time
            ref = DeferredReference(
                target_type=entry.link_target,
                value=actual_id,
                source_file=source_frame.filename,
                source_line=source_frame.lineno,
                source_code=source_frame.line or "",
                attribute_name=name,
            )
            serializer.add_deferred(ref)
            value = actual_id
        
        # VALIDATION: Enum/Bitmask types (immediate)
        elif entry and entry.is_enum:
            manifest.validate_enum_value(entry, value, source_info)
        
        # Set the value on component or unit
        comp = self._find_component(name)
        if comp:
            for u in units:
                obj = getattr(u, comp, None)
                if obj is not None:
                    setattr(obj, name, value)
            return

        # Direct Unit attribute
        if hasattr(units[0], name):
            for u in units:
                setattr(u, name, value)
            return

        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

