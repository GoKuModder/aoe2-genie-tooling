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

# Wrapper imports (modernized versions)
from Actual_Tools_GDP.Units.wrappers import (
    CombatWrapper as Type50Wrapper, 
    CreationWrapper as CreatableWrapper, 
    MovementWrapper as DeadFishWrapper,
    BehaviorWrapper as BirdWrapper, 
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

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["UnitHandle"]

# Component names for flattening lookup (OLD style names for wrapper compatibility)
_COMPONENTS = ("bird", "dead_fish", "type_50", "projectile", "creatable", "building")


class UnitHandle:
    """
    High-level wrapper for Genie Unit objects with full attribute flattening.

    All attributes from Unit, Bird, DeadFish, Type50, Projectile, Creatable,
    and Building are accessible directly on this object.

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
        # Wrapper caches
        "_combat_cache", "_creatable_cache", "_cost_cache", "_dead_fish_cache",
        "_bird_cache", "_projectile_cache", "_building_cache",
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
        # Initialize wrapper caches to None
        object.__setattr__(self, "_combat_cache", None)
        object.__setattr__(self, "_creatable_cache", None)
        object.__setattr__(self, "_cost_cache", None)
        object.__setattr__(self, "_dead_fish_cache", None)
        object.__setattr__(self, "_bird_cache", None)
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
        object.__setattr__(self, "_creatable_cache", None)
        object.__setattr__(self, "_cost_cache", None)
        object.__setattr__(self, "_dead_fish_cache", None)
        object.__setattr__(self, "_bird_cache", None)
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
    def type_50(self) -> Type50Wrapper:
        """Type50 wrapper (alias for combat). Cached."""
        return self.combat

    @property
    def creatable(self) -> CreatableWrapper:
        """Creatable wrapper. Cached."""
        if self._creatable_cache is None:
            object.__setattr__(self, "_creatable_cache", CreatableWrapper(self._get_units()))
        return self._creatable_cache

    @property
    def cost(self) -> CostWrapper:
        """Cost wrapper. Cached."""
        if self._cost_cache is None:
            object.__setattr__(self, "_cost_cache", CostWrapper(self._get_units()))
        return self._cost_cache

    @property
    def dead_fish(self) -> DeadFishWrapper:
        """DeadFish wrapper. Cached."""
        if self._dead_fish_cache is None:
            object.__setattr__(self, "_dead_fish_cache", DeadFishWrapper(self._get_units()))
        return self._dead_fish_cache

    @property
    def bird(self) -> BirdWrapper:
        """Bird wrapper. Cached."""
        if self._bird_cache is None:
            object.__setattr__(self, "_bird_cache", BirdWrapper(self._get_units()))
        return self._bird_cache

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

    def __getattr__(self, name: str) -> Any:
        # Don't intercept internal attributes
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        u = self._primary_unit
        if not u:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}' (no units)")

        # Direct Unit attribute
        if hasattr(u, name) and name not in _COMPONENTS:
            return getattr(u, name)

        # Sub-component attribute
        comp = self._find_component(name)
        if comp:
            # Use the wrapper instance from self
            return getattr(getattr(self, comp), name)

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
        
        # Try to import manifest loader for validation (may not exist yet)
        try:
            from Actual_Tools_GDP.Shared.manifest_loader import manifest, serializer, DeferredReference
            has_manifest = True
        except ImportError:
            has_manifest = False
            manifest = None

        if has_manifest and manifest:
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
