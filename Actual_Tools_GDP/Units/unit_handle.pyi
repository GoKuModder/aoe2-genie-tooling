"""
Type stubs for UnitHandle - Provides strict IDE validation and autocomplete.
Unlike the runtime class, this stub does not permit arbitrary attribute assignment.
"""
from typing import List, Optional, Tuple, Any, Union

from Actual_Tools_GDP.Base.workspace import GenieWorkspace
from Actual_Tools_GDP.Units.task_builder import TaskBuilder

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

from Actual_Tools_GDP.Units.unit_collections import (
    TasksManager,
    AttacksManager,
    ArmoursManager,
    DamageGraphicsManager,
    TrainLocationsManager,
    DropSitesManager,
    AnnexesManager,
    CostsManager,
    ResourcesManager
)

class UnitHandle:
    # --------------------------------------------------------------------------
    # Core Attributes
    # --------------------------------------------------------------------------
    id: int
    unit_id: int
    name: str
    
    # Basic Stats
    type_: int
    enabled: int
    disabled: int
    class_: int
    hit_points: int
    line_of_sight: float
    garrison_capacity: int
    speed: float
    
    # String IDs
    name_str_id: int
    creation_str_id: int
    help_str_id: int
    hotkey_text_str_id: int
    hotkey_str_id: int
    
    # Graphics
    trait: int
    trait_piece: int
    standing_sprite_id1: int
    standing_sprite_id2: int
    dying_sprite_id: int
    undead_sprite_id: int
    icon_id: int
    
    # Dimensions
    radius_x: float
    radius_y: float
    radius_z: float
    selection_radius_x: float
    selection_radius_y: float
    selection_radius_z: float
    selection_effect: int
    editor_selection_color: int
    
    # Sounds
    train_sound_id: int
    damage_sound_id1: int
    selection_sound_id: int
    dying_sound_id: int
    wwise_train_sound_id: int
    wwise_damage_sound_id: int
    wwise_selection_sound_id: int
    wwise_dying_sound_id: int
    
    # Death/Corpse
    dead_unit_id: int
    blood_unit_id: int
    undead_mode: int
    
    # Terrain & Placement
    can_be_built_on: int
    required_side_terrain_id1: int
    required_side_terrain_id2: int
    required_center_terrain_id1: int
    required_center_terrain_id2: int
    required_clearance_radius_x: float
    required_clearance_radius_y: float
    elevation_restriction_mode: int
    terrain_restriction_id: int
    foundation_terrain_id: int
    
    # Movement & Pathfinding Core
    movement_mode: int
    obstruction_type: int
    obstruction_class: int
    
    # Resources
    resource_carry_capacity: int
    resource_decay_rate: float
    resource_gather_group: int
    enable_auto_gather: int
    
    # Combat Core
    blast_defense_level: int
    combat_level: int
    old_attack_mode: int
    
    # Display & Modes
    interaction_mode: int
    minimap_mode: int
    interface_mode: int
    minimap_color: int
    fog_visibility_mode: int
    occlusion_mode: int
    
    # Misc
    sort_number: int
    hide_in_editor: int
    multiple_attribute_mode: float
    recyclable: int
    doppelganger_mode: int
    convert_terrain: int

    # --------------------------------------------------------------------------
    # Wrapper Accessors
    # --------------------------------------------------------------------------
    @property
    def combat(self) -> CombatWrapper: ...
    @property
    def creation(self) -> CreationWrapper: ...
    @property
    def cost(self) -> CostsManager: ...  # Wrapper points to CostsManager via property in unit_handle.py
    
    @property
    def movement(self) -> MovementWrapper: ...
    @property
    def behavior(self) -> BehaviorWrapper: ...
    @property
    def projectile(self) -> ProjectileWrapper: ...
    @property
    def building(self) -> BuildingWrapper: ...
    
    @property
    def resource_storages(self) -> ResourcesManager: ...
    @property
    def resources(self) -> ResourcesManager: ...
    
    @property
    def damage_graphics(self) -> DamageGraphicsManager: ...
    @property
    def train_locations_wrapper(self) -> TrainLocationsManager: ...
    
    @property
    def tasks(self) -> TasksManager: ...
    @property
    def tasks_wrapper(self) -> TasksManager: ...

    # --------------------------------------------------------------------------
    # Flattened BuildingWrapper
    # --------------------------------------------------------------------------
    construction_graphic_id: int
    snow_graphic_id: int
    destruction_graphic_id: int
    destruction_rubble_graphic_id: int
    research_graphic_id: int
    research_complete_graphic_id: int
    adjacent_mode: int
    graphics_angle: int
    disappears_when_built: int
    stack_unit_id: int
    # foundation_terrain_id defined in core
    old_overlap_id: int
    tech_id: int
    completion_tech_id: int
    can_burn: int
    head_unit_id: int
    transform_unit_id: int
    salvage_unit_id: int
    pile_unit_id: int
    transform_sound_id: int
    construction_sound_id: int
    wwise_transform_sound_id: int
    wwise_construction_sound_id: int
    garrison_type: int
    garrison_heal_rate: float
    garrison_repair_rate: float
    looting_table: Any
    annexes: AnnexesManager
    annexes_manager: AnnexesManager

    # --------------------------------------------------------------------------
    # Flattened CombatWrapper
    # --------------------------------------------------------------------------
    attack_graphic_id: int
    attack_graphic_2_id: int
    max_range: float
    min_range: float
    reload_time: float
    accuracy_percent: int
    accuracy_dispersion: float
    blast_width: float
    blast_damage: float
    blast_attack_level: int
    frame_delay: int
    break_off_combat: int
    base_armor: int
    defense_terrain_bonus: int
    bonus_damage_resistance: float
    damage_reflection: float
    friendly_fire_damage: float
    displayed_attack: int
    displayed_melee_armour: int
    displayed_range: float
    displayed_reload_time: float
    projectile_unit_id: int
    graphic_displacement: Tuple[float, float, float]
    weapon_offset_x: float
    weapon_offset_y: float
    weapon_offset_z: float
    interrupt_frame: int
    garrison_firepower: float
    # attacks: AttacksManager # defined below with methods
    # armours: ArmoursManager

    # --------------------------------------------------------------------------
    # Flattened CreationWrapper
    # --------------------------------------------------------------------------
    train_time: int
    train_location_id: int
    button_id: int
    hot_key_id: int
    # train_locations: TrainLocationsManager
    # resource_costs: CostsManager
    # costs: CostsManager
    garrison_graphic_id: int
    spawning_graphic_id: int
    upgrade_graphic_id: int
    hero_glow_graphic_id: int
    idle_attack_graphic_id: int
    special_graphic_id: int
    max_charge: float
    recharge_rate: float
    charge_event: int
    charge_type: int
    charge_target: int
    charge_projectile_unit_id: int
    rear_attack_modifier: float
    flank_attack_modifier: float
    attack_priority: int
    invulnerability_level: float
    min_conversion_time_mod: float
    max_conversion_time_mod: float
    conversion_chance_mod: float
    total_projectiles: float
    max_total_projectiles: int
    secondary_projectile_unit_id: int
    projectile_spawning_area: Tuple[float, float, float]
    projectile_spawning_area_width: float
    projectile_spawning_area_length: float
    projectile_spawning_area_randomness: float
    button_icon_id: int
    button_short_tooltip_id: int
    button_extended_tooltip_id: int
    button_hotkey_action: int
    creatable_type: int
    hero_mode: int
    special_ability: int
    displayed_pierce_armour: int

    # --------------------------------------------------------------------------
    # Flattened MovementWrapper
    # --------------------------------------------------------------------------
    walking_graphic_id: int
    running_graphic_id: int
    rotation_speed: float
    turn_radius: float
    rotation_radius: float
    turn_radius_speed: float
    rotation_radius_speed: float
    max_yaw_per_second_moving: float
    max_yaw_per_sec_walking: float
    stationary_yaw_revolution_time: float
    standing_yaw_revolution_time: float
    max_yaw_per_second_stationary: float
    max_yaw_per_sec_standing: float
    tracking_unit_id: int
    trailing_unit_id: int
    tracking_unit_mode: int
    trail_mode: int
    tracking_unit_density: float
    trail_spacing: float
    old_size_class: int
    old_move_algorithm: int
    min_collision_size_multiplier: float

    # --------------------------------------------------------------------------
    # Flattened BehaviorWrapper
    # --------------------------------------------------------------------------
    default_task_id: int
    search_radius: float
    work_rate: float
    task_swap_group: int
    run_mode: int
    run_pattern: int
    # tasks: TasksManager
    # drop_sites: DropSitesManager
    drop_site_unit_ids: DropSitesManager
    attack_sound_id: int
    attack_sound: int
    move_sound_id: int
    move_sound: int
    wwise_attack_sound_id: int
    wwise_move_sound_id: int

    # --------------------------------------------------------------------------
    # Flattened ProjectileWrapper
    # --------------------------------------------------------------------------
    projectile_type: int
    smart_mode: int
    hit_mode: int
    vanish_mode: int
    area_effect_specials: int
    projectile_arc: float

    # --------------------------------------------------------------------------
    # Collection Accessors (Flattened)
    # --------------------------------------------------------------------------
    @property
    def attacks(self) -> AttacksManager: ...
    @attacks.setter
    def attacks(self, value: List[Any]) -> None: ...
    
    @property
    def armours(self) -> ArmoursManager: ...
    @armours.setter
    def armours(self, value: List[Any]) -> None: ...
    
    @property
    def resource_costs(self) -> CostsManager: ...
    @resource_costs.setter
    def resource_costs(self, value: List[Any]) -> None: ...
    
    @property
    def costs(self) -> CostsManager: ...
    @costs.setter
    def costs(self, value: List[Any]) -> None: ...
    
    @property
    def train_locations(self) -> TrainLocationsManager: ...
    @train_locations.setter
    def train_locations(self, value: List[Any]) -> None: ...
    
    @property
    def drop_sites(self) -> DropSitesManager: ...
    @drop_sites.setter
    def drop_sites(self, value: List[int]) -> None: ...
    
    # --------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------
    def __init__(self, workspace: GenieWorkspace, unit_id: int, civ_ids: Optional[List[int]] = None) -> None: ...
    
    def invalidate_cache(self) -> None: ...
    
    # Resource Storage
    def resource_1(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None: ...
    def resource_2(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None: ...
    def resource_3(self, type: int = 0, amount: float = 0.0, flag: int = 0) -> None: ...
    
    # Attacks
    def add_attack(self, class_: int, amount: int) -> Optional[AttackHandle]: ...
    def get_attack_by_id(self, attack_id: int) -> Optional[AttackHandle]: ...
    def get_attack_by_class(self, class_: int) -> Optional[AttackHandle]: ...
    def remove_attack(self, attack_id: int) -> bool: ...
    def set_attack(self, class_: int, amount: int) -> Optional[AttackHandle]: ...
    
    # Armours
    def add_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]: ...
    def get_armour_by_id(self, armour_id: int) -> Optional[ArmourHandle]: ...
    def get_armour_by_class(self, class_: int) -> Optional[ArmourHandle]: ...
    def remove_armour(self, armour_id: int) -> bool: ...
    def set_armour(self, class_: int, amount: int) -> Optional[ArmourHandle]: ...
    
    # Damage Graphics
    def add_damage_graphic(self, graphic_id: int, damage_percent: int, apply_mode: int = 0) -> Optional[DamageGraphicHandle]: ...
    def get_damage_graphic(self, damage_graphic_id: int) -> Optional[DamageGraphicHandle]: ...
    def remove_damage_graphic(self, damage_graphic_id: int) -> bool: ...
    
    # Tasks
    @property
    def add_task(self) -> TaskBuilder: ...
    
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
    ) -> Optional[TaskHandle]: ...
    
    def get_task(self, task_id: int) -> Optional[TaskHandle]: ...
    def get_tasks_list(self) -> List[TaskHandle]: ...
    def remove_task(self, task_id: int) -> bool: ...
    
    # Train Locations
    def add_train_location(
        self,
        unit_id: int,
        train_time: int = 0,
        button_id: int = 0,
        hot_key_id: int = 0,
    ) -> Optional[TrainLocationHandle]: ...
    
    def get_train_location(self, train_location_id: int) -> Optional[TrainLocationHandle]: ...
    def remove_train_location(self, train_location_id: int) -> bool: ...
    
    # Drop Sites
    def add_drop_site(self, unit_id: int) -> Optional[DropSiteHandle]: ...
    def get_drop_site(self, drop_site_id: int) -> Optional[DropSiteHandle]: ...
    def remove_drop_site(self, drop_site_id: int) -> bool: ...
