"""Type stubs for UnitHandle - provides IDE autocomplete for flattened attributes."""
from typing import List, Optional, Tuple

from genieutils.unit import AttackOrArmor, ResourceStorage, DamageGraphic, BuildingAnnex, ResourceCost, TrainLocation
from genieutils.task import Task as GenieTask

from Actual_Tools.Units.handles import (
    TaskHandle, AttackHandle, ArmourHandle, DamageGraphicHandle,
    TrainLocationHandle, DropSiteHandle
)
from Actual_Tools.Units.wrappers import (
    Type50Wrapper, CreatableWrapper, CostWrapper, DeadFishWrapper,
    BirdWrapper, ProjectileWrapper, BuildingWrapper, ResourceStoragesWrapper,
    DamageGraphicsWrapper, TasksWrapper
)

class UnitHandle:
    # Basic
    id: int
    name: str
    
    # Wrappers
    combat: Type50Wrapper
    creatable: CreatableWrapper
    cost: CostWrapper
    dead_fish: DeadFishWrapper
    bird: BirdWrapper
    projectile: ProjectileWrapper
    building: BuildingWrapper
    resource_storages: ResourceStoragesWrapper
    damage_graphics: DamageGraphicsWrapper
    tasks: TasksWrapper
    
    # UNIT DIRECT ATTRIBUTES
    type: int
    hit_points: int
    line_of_sight: float
    garrison_capacity: int
    speed: Optional[float]
    class_: int
    train_sound: int
    damage_sound: int
    icon_id: int
    enabled: int
    
    # BIRD ATTRIBUTES (flattened)
    default_task_id: int
    search_radius: float
    work_rate: float
    attack_sound: int
    move_sound: int
    
    # DEAD_FISH ATTRIBUTES (flattened)
    walking_graphic: int
    rotation_speed: float
    
    # TYPE50 ATTRIBUTES (flattened)
    base_armor: int
    max_range: float
    reload_time: float
    projectile_unit_id: int
    attack_graphic: int
    
    # PROJECTILE ATTRIBUTES (flattened)
    projectile_type: int
    smart_mode: int
    hit_mode: int
    vanish_mode: int
    
    # CREATABLE ATTRIBUTES (flattened)
    hero_mode: int
    garrison_graphic: int
    
    # BUILDING ATTRIBUTES (flattened)
    construction_graphic_id: int
    garrison_type: int
    tech_id: int
    
    # Collections
    attacks: List[AttackOrArmor]
    armours: List[AttackOrArmor]
    resource_costs: Tuple[ResourceCost, ResourceCost, ResourceCost]
    train_locations: List[TrainLocation]
    annexes: Tuple[BuildingAnnex, ...]
    looting_table: Tuple[int, ...]
    drop_sites: List[int]
    
    # Resource storage methods
    def resource_1(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None: ...
    def resource_2(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None: ...
    def resource_3(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None: ...
    
    # Attack methods
    def add_attack(self, class_: int, amount: int) -> Optional[AttackHandle]: ...
    def get_attack_by_id(self, attack_id: int) -> Optional[AttackHandle]: ...
    def get_attack_by_class(self, class_: int) -> Optional[AttackHandle]: ...
    def remove_attack(self, attack_id: int) -> bool: ...
    def set_attack(self, class_: int, amount: int) -> Optional[AttackHandle]: ...
    
    # Armour methods
    def add_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]: ...
    def get_armour_by_id(self, armour_id: int) -> Optional[ArmourHandle]: ...
    def get_armour_by_class(self, class_: int) -> Optional[ArmourHandle]: ...
    def remove_armour(self, armour_id: int) -> bool: ...
    def set_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]: ...
    
    # Damage graphic methods
    def add_damage_graphic(self, graphic_id: int, damage_percent: int, apply_mode: int = 0) -> Optional[DamageGraphicHandle]: ...
    def get_damage_graphic(self, damage_graphic_id: int) -> Optional[DamageGraphicHandle]: ...
    def remove_damage_graphic(self, damage_graphic_id: int) -> bool: ...
    
    # Task methods
    def add_task(self, task_type: int = 0, id: int = 0, is_default: int = 0, action_type: int = 0, class_id: int = -1, unit_id: int = -1, terrain_id: int = -1, resource_in: int = -1, resource_out: int = -1, work_value_1: float = 0.0, work_value_2: float = 0.0, work_range: float = 0.0, enabled: int = 1, **kwargs) -> Optional[TaskHandle]: ...
    def get_task(self, task_id: int) -> Optional[TaskHandle]: ...
    def get_tasks_list(self) -> List[TaskHandle]: ...
    def remove_task(self, task_id: int) -> bool: ...
    
    # Train location methods
    def add_train_location(self, unit_id: int, train_time: int = 0, button_id: int = 0, hot_key_id: int = 0) -> Optional[TrainLocationHandle]: ...
    def get_train_location(self, train_location_id: int) -> Optional[TrainLocationHandle]: ...
    def remove_train_location(self, train_location_id: int) -> bool: ...
    
    # Drop site methods
    def add_drop_site(self, unit_id: int) -> Optional[DropSiteHandle]: ...
    def get_drop_site(self, drop_site_id: int) -> Optional[DropSiteHandle]: ...
    def remove_drop_site(self, drop_site_id: int) -> bool: ...
