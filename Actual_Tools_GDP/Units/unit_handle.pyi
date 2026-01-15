"""Type stubs for UnitHandle - provides IDE autocomplete for flattened attributes.

This comprehensive stub file includes all 269+ attributes from:
- Unit main class
- CombatWrapper (combat/type_50)  
- MovementWrapper (dead_fish)
- BehaviorWrapper (bird)
- ProjectileWrapper (projectile)
- CreationWrapper (creatable)
- BuildingWrapper (building)
"""
from typing import List, Optional, Tuple, Any

from Actual_Tools_GDP.Units.handles import (
    TaskHandle, AttackHandle, ArmourHandle, DamageGraphicHandle,
    TrainLocationHandle, DropSiteHandle
)
from Actual_Tools_GDP.Units.wrappers import (
    CombatWrapper as Type50Wrapper,
    CreationWrapper as CreatableWrapper,
    MovementWrapper as DeadFishWrapper,
    BehaviorWrapper as BirdWrapper,
    ProjectileWrapper,
    BuildingWrapper
)
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
from Actual_Tools_GDP.Units.task_builder import TaskBuilder


class UnitHandle:
    """Unit handle with full attribute flattening for IDE autocomplete."""
    
    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================
    id: int
    unit_id: int
    name: str
    
    # =========================================================================
    # WRAPPER REFERENCES
    # =========================================================================
    combat: Type50Wrapper
    type_50: Type50Wrapper
    creatable: CreatableWrapper
    cost: CostWrapper
    dead_fish: DeadFishWrapper
    bird: BirdWrapper
    projectile: ProjectileWrapper
    building: BuildingWrapper
    resource_storages: ResourceStoragesWrapper
    damage_graphics: DamageGraphicsWrapper
    tasks: TasksWrapper
    tasks_wrapper: TasksWrapper
    train_locations_wrapper: TrainLocationsWrapper
    
    # =========================================================================
    # UNIT MAIN ATTRIBUTES (directly from Unit)
    # =========================================================================
    
    # String IDs
    name_str_id: int
    creation_str_id: int
    help_str_id: int
    hotkey_text_str_id: int
    hotkey_str_id: int
    
    # Graphics/Sprites  
    trait: int
    trait_piece: int
    standing_sprite_id1: int
    standing_sprite_id2: int
    dying_sprite_id: int
    undead_sprite_id: int
    icon_id: int
    
    # Physical Dimensions
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
    
    # Placement/Terrain
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
    
    # Movement/Pathfinding
    movement_mode: int
    obstruction_type: int
    obstruction_class: int
    
    # Resources/Economy
    resource_carry_capacity: int
    resource_decay_rate: float
    resource_gather_group: int
    enable_auto_gather: int
    
    # Combat/Interaction
    blast_defense_level: int
    combat_level: int
    old_attack_mode: int
    
    # Display/Interface
    interaction_mode: int
    minimap_mode: int
    interface_mode: int
    minimap_color: int
    fog_visibility_mode: int
    occlusion_mode: int
    
    # Miscellaneous
    sort_number: int
    hide_in_editor: int
    multiple_attribute_mode: float
    recyclable: int
    doppelganger_mode: int
    convert_terrain: int
    
    # Missing Unit attributes frequently used
    type_: int
    enabled: int
    disabled: int
    class_: int
    hit_points: int
    line_of_sight: float
    garrison_capacity: int
    speed: Optional[float]
    
    # =========================================================================
    # COMBAT WRAPPER ATTRIBUTES (flattened from combat/type_50)
    # =========================================================================
    
    # Attack Properties
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
    
    # Armor Properties
    base_armor: int
    defense_terrain_bonus: int
    bonus_damage_resistance: float
    damage_reflection: float
    friendly_fire_damage: float
    
    # Display Properties
    displayed_attack: int
    displayed_melee_armour: int
    displayed_range: float
    displayed_reload_time: float
    
    # Projectile Properties
    projectile_unit_id: int
    weapon_offset_x: float
    weapon_offset_y: float
    weapon_offset_z: float
    graphic_displacement: Tuple[float, float, float]
    interrupt_frame: int
    garrison_firepower: float
    
    # =========================================================================
    # MOVEMENT WRAPPER ATTRIBUTES (flattened from dead_fish)
    # =========================================================================
    
    # Graphics
    walking_graphic_id: int
    running_graphic_id: int
    
    # Rotation/Turning
    rotation_speed: float
    turn_radius: float
    rotation_radius: float
    turn_radius_speed: float
    rotation_radius_speed: float
    
    # Yaw/Rotation Timing
    max_yaw_per_second_moving: float
    max_yaw_per_sec_walking: float
    stationary_yaw_revolution_time: float
    standing_yaw_revolution_time: float
    max_yaw_per_second_stationary: float
    max_yaw_per_sec_standing: float
    
    # Tracking/Trailing
    tracking_unit_id: int
    trailing_unit_id: int
    tracking_unit_mode: int
    tracking_unit_density: float
    trail_mode: int
    trail_spacing: float
    
    # Miscellaneous Movement
    old_size_class: int
    old_move_algorithm: int
    min_collision_size_multiplier: float
    
    # =========================================================================
    # BEHAVIOR WRAPPER ATTRIBUTES (flattened from bird)
    # =========================================================================
    
    # Behavior Properties
    default_task_id: int
    search_radius: float
    work_rate: float
    task_swap_group: int
    run_mode: int
    run_pattern: int
    
    # Sound Properties
    attack_sound_id: int
    attack_sound: int
    move_sound_id: int
    move_sound: int
    wwise_attack_sound_id: int
    wwise_move_sound_id: int
    
    # Drop Sites (scalar property)
    drop_site_unit_ids: List[int]
    
    # =========================================================================
    # PROJECTILE WRAPPER ATTRIBUTES (flattened from projectile)
    # =========================================================================
    
    projectile_type: int
    smart_mode: int
    hit_mode: int
    vanish_mode: int
    area_effect_specials: int
    projectile_arc: float
    
    # =========================================================================
    # CREATION WRAPPER ATTRIBUTES (flattened from creatable)
    # =========================================================================
    
    # Training Properties
    train_time: int
    train_location_id: int
    button_id: int
    hot_key_id: int
    creatable_type: int
    
    # Graphics
    garrison_graphic_id: int
    spawning_graphic_id: int
    upgrade_graphic_id: int
    hero_glow_graphic_id: int
    idle_attack_graphic_id: int
    special_graphic_id: int
    
    # Hero Properties
    hero_mode: int
    
    # Charge Properties
    max_charge: float
    recharge_rate: float
    charge_event: int
    charge_type: int
    charge_target: int
    charge_projectile_unit_id: int
    
    # Conversion Properties
    min_conversion_time_mod: float
    max_conversion_time_mod: float
    conversion_chance_mod: float
    
    # Projectile Properties
    total_projectiles: int
    max_total_projectiles: int
    secondary_projectile_unit_id: int
    projectile_spawning_area: float
    projectile_spawning_area_width: float
    projectile_spawning_area_length: float
    projectile_spawning_area_randomness: float
    
    # Combat Modifiers
    rear_attack_modifier: float
    flank_attack_modifier: float
    displayed_pierce_armour: int
    
    # UI Properties
    button_icon_id: int
    button_short_tooltip_id: int
    button_extended_tooltip_id: int
    button_hotkey_action: int
    
    # Miscellaneous
    attack_priority: int
    invulnerability_level: int
    special_ability: int
    
    # =========================================================================
    # BUILDING WRAPPER ATTRIBUTES (flattened from building)
    # =========================================================================
    
    # Graphics
    construction_graphic_id: int
    snow_graphic_id: int
    destruction_graphic_id: int
    destruction_rubble_graphic_id: int
    research_graphic_id: int
    research_complete_graphic_id: int
    
    # Building Modes
    adjacent_mode: int
    graphics_angle: int
    disappears_when_built: int
    can_burn: int
    
    # Stacking/Transform
    stack_unit_id: int
    head_unit_id: int
    pile_unit_id: int
    transform_unit_id: int
    transform_sound_id: int
    wwise_transform_sound_id: int
    
    # Garrison
    garrison_type: int
    garrison_heal_rate: float
    garrison_repair_rate: float
    
    # Tech
    tech_id: int
    completion_tech_id: int
    
    # Construction
    construction_sound_id: int
    wwise_construction_sound_id: int
    
    # Salvage
    salvage_unit_id: int
    looting_table: Any
    
    # Miscellaneous
    old_overlap_id: int
    
    # =========================================================================
    # COLLECTION MANAGERS
    # =========================================================================
    
    attacks: AttacksManager
    armours: ArmoursManager
    resource_costs: CostWrapper
    costs: CostWrapper
    resources: ResourceStoragesWrapper
    train_locations: TrainLocationsWrapper
    annexes: AnnexesManager
    drop_sites: DropSitesManager
    
    # =========================================================================
    # METHODS
    # =========================================================================
    
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
    @property
    def add_task(self) -> TaskBuilder:
        """
        Fluent API for adding typed tasks.
        
        Usage:
            unit.add_task.combat(class_id=0)
            unit.add_task.garrison(class_id=11)
            unit.add_task.aura(work_value_1=10, work_range=5)
        """
        ...
    
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
        """Add task with raw parameters. Use add_task property for typed API."""
        ...
    
    def get_task(self, task_id: int) -> Optional[TaskHandle]: ...
    def get_tasks_list(self) -> List[TaskHandle]: ...
    def remove_task(self, task_id: int) -> bool: ...
    
    # Train location methods
    def add_train_location(
        self,
        unit_id: int,
        train_time: int = 0,
        button_id: int = 0,
        hot_key_id: int = 0
    ) -> Optional[TrainLocationHandle]: ...
    def get_train_location(self, train_location_id: int) -> Optional[TrainLocationHandle]: ...
    def remove_train_location(self, train_location_id: int) -> bool: ...
    
    # Drop site methods
    def add_drop_site(self, unit_id: int) -> Optional[DropSiteHandle]: ...
    def get_drop_site(self, drop_site_id: int) -> Optional[DropSiteHandle]: ...
    def remove_drop_site(self, drop_site_id: int) -> bool: ...
    
    # Validation
    def validate_all_references(self) -> list: ...
    
    # Utility
    def invalidate_cache(self) -> None: ...
