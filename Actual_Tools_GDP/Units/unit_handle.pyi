"""Type stubs for UnitHandle - ONLY shows the curated API, not raw GenieDatParser attributes.

This ensures IDE autocomplete shows ONLY the attributes you've explicitly exposed,
preventing confusion with underlying GenieDatParser attributes.
"""
from typing import List, Optional, Any

# Import wrapper classes
from Actual_Tools_GDP.Units.wrappers.combat import CombatWrapper
from Actual_Tools_GDP.Units.wrappers.movement import MovementWrapper as DeadFishWrapper
from Actual_Tools_GDP.Units.wrappers.behavior import BehaviorWrapper as BirdWrapper
from Actual_Tools_GDP.Units.wrappers.projectile import ProjectileWrapper
from Actual_Tools_GDP.Units.wrappers.creation import CreationWrapper as CreatableWrapper
from Actual_Tools_GDP.Units.wrappers.building import BuildingWrapper

# Import collection managers (if they exist)
try:
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
except ImportError:
    TasksManager = Any
    AttacksManager = Any
    ArmoursManager = Any
    DamageGraphicsManager = Any
    TrainLocationsManager = Any
    DropSitesManager = Any
    AnnexesManager = Any
    CostsManager = Any
    ResourcesManager = Any

# Import handles
from Actual_Tools_GDP.Units.handles import (
    TaskHandle, AttackHandle, ArmourHandle, DamageGraphicHandle,
    TrainLocationHandle, DropSiteHandle
)
from Actual_Tools_GDP.Units.task_builder import TaskBuilder

class UnitHandle:
    """
    UnitHandle - Curated API for Age of Empires 2 unit editing.
    
    This stub file shows ONLY the explicitly exposed API.
    IDE will flag any attributes not listed here as errors.
    """
    
    # =========================================================================
    # BASIC PROPERTIES (Explicitly defined in UnitHandle)
    # =========================================================================
    id: int
    unit_id: int
    name: str
    type_: int
    enabled: int
    disabled: int
    class_: int
    hit_points: int
    line_of_sight: float
    garrison_capacity: int
    speed: Optional[float]
    
    # =========================================================================
    # WRAPPER REFERENCES (Modernized)
    # =========================================================================
    combat: CombatWrapper
    behavior: BehaviorWrapper
    movement: MovementWrapper
    projectile: ProjectileWrapper
    creatable: CreatableWrapper
    building: BuildingWrapper
    
    # Legacy Aliases
    type_50: CombatWrapper
    bird: BehaviorWrapper
    dead_fish: MovementWrapper
    
    # =========================================================================
    # COLLECTION MANAGERS
    # =========================================================================
    tasks: TasksManager
    attacks: AttacksManager
    armours: ArmoursManager
    damage_graphics: DamageGraphicsManager
    train_locations: TrainLocationsManager
    drop_sites: DropSitesManager
    annexes: AnnexesManager
    resources: ResourcesManager
    resource_storages: ResourcesManager  # Alias
    
    # =========================================================================
    # UNIT MAIN ATTRIBUTES - ONLY THOSE IN YOUR API
    # From UnitHandle_API_Attributes.md
    # =========================================================================
    
    # String IDs
    name_str_id: int
    creation_str_id: int
    help_str_id: int
    hotkey_text_str_id: int
    hotkey_str_id: int
    
    # Graphics/Sprites (only those explicitly in your API)
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
    
    # =========================================================================
    # COMBAT WRAPPER ATTRIBUTES (flattened)
    # =========================================================================
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
    weapon_offset_x: float
    weapon_offset_y: float
    weapon_offset_z: float
    interrupt_frame: int
    garrison_firepower: float
    
    # =========================================================================
    # MOVEMENT WRAPPER ATTRIBUTES (flattened)
    # =========================================================================
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
    tracking_unit_density: float
    trail_mode: int
    trail_spacing: float
    old_size_class: int
    old_move_algorithm: int
    min_collision_size_multiplier: float
    
    # =========================================================================
    # BEHAVIOR WRAPPER ATTRIBUTES (flattened)
    # =========================================================================
    default_task_id: int
    search_radius: float
    work_rate: float
    task_swap_group: int
    run_mode: int
    run_pattern: int  # Alias for run_mode
    attack_sound_id: int
    attack_sound: int  # Alias
    move_sound_id: int
    move_sound: int  # Alias
    wwise_attack_sound_id: int
    wwise_move_sound_id: int
    drop_site_unit_ids: List[int]
    
    # =========================================================================
    # PROJECTILE WRAPPER ATTRIBUTES (flattened)
    # =========================================================================
    projectile_type: int
    smart_mode: int
    hit_mode: int
    vanish_mode: int
    area_effect_specials: int
    projectile_arc: float
    
    # =========================================================================
    # CREATION WRAPPER ATTRIBUTES (flattened)
    # =========================================================================
    train_time: int
    train_location_id: int
    button_id: int
    hot_key_id: int
    creatable_type: int
    garrison_graphic_id: int
    spawning_graphic_id: int
    upgrade_graphic_id: int
    hero_glow_graphic_id: int
    idle_attack_graphic_id: int
    special_graphic_id: int
    hero_mode: int
    max_charge: float
    recharge_rate: float
    charge_event: int
    charge_type: int
    charge_target: int
    charge_projectile_unit_id: int
    min_conversion_time_mod: float
    max_conversion_time_mod: float
    conversion_chance_mod: float
    total_projectiles: int
    max_total_projectiles: int
    secondary_projectile_unit_id: int
    projectile_spawning_area: float
    projectile_spawning_area_width: float
    projectile_spawning_area_length: float
    projectile_spawning_area_randomness: float
    rear_attack_modifier: float
    flank_attack_modifier: float
    displayed_pierce_armour: int
    button_icon_id: int
    button_short_tooltip_id: int
    button_extended_tooltip_id: int
    button_hotkey_action: int
    attack_priority: int
    invulnerability_level: int
    special_ability: int
    
    # =========================================================================
    # BUILDING WRAPPER ATTRIBUTES (flattened)
    # =========================================================================
    construction_graphic_id: int
    snow_graphic_id: int
    destruction_graphic_id: int
    destruction_rubble_graphic_id: int
    research_graphic_id: int
    research_complete_graphic_id: int
    adjacent_mode: int
    graphics_angle: int
    disappears_when_built: int
    can_burn: int
    stack_unit_id: int
    head_unit_id: int
    pile_unit_id: int
    transform_unit_id: int
    transform_sound_id: int
    wwise_transform_sound_id: int
    garrison_type: int
    garrison_heal_rate: float
    garrison_repair_rate: float
    tech_id: int
    completion_tech_id: int
    construction_sound_id: int
    wwise_construction_sound_id: int
    salvage_unit_id: int
    looting_table: Any
    old_overlap_id: int
    
    # =========================================================================
    # METHODS (For reference - IDE will show these)
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

# =========================================================================
# FLATTENED PROPERTY STUBS 
# =========================================================================

    # CombatWrapper flattened properties
    @property
    def accuracy_dispersion(self) -> float: ...
    @accuracy_dispersion.setter
    def accuracy_dispersion(self, value: float) -> None: ...

    @property
    def accuracy_percent(self) -> int: ...
    @accuracy_percent.setter
    def accuracy_percent(self, value: int) -> None: ...

    @property
    def armours(self) -> Any: ...
    @armours.setter
    def armours(self, value: Any) -> None: ...

    @property
    def attack_graphic_2_id(self) -> int: ...
    @attack_graphic_2_id.setter
    def attack_graphic_2_id(self, value: int) -> None: ...

    @property
    def attack_graphic_id(self) -> int: ...
    @attack_graphic_id.setter
    def attack_graphic_id(self, value: int) -> None: ...

    @property
    def attacks(self) -> Any: ...
    @attacks.setter
    def attacks(self, value: Any) -> None: ...

    @property
    def base_armor(self) -> int: ...
    @base_armor.setter
    def base_armor(self, value: int) -> None: ...

    @property
    def blast_attack_level(self) -> int: ...
    @blast_attack_level.setter
    def blast_attack_level(self, value: int) -> None: ...

    @property
    def blast_damage(self) -> float: ...
    @blast_damage.setter
    def blast_damage(self, value: float) -> None: ...

    @property
    def blast_width(self) -> float: ...
    @blast_width.setter
    def blast_width(self, value: float) -> None: ...

    @property
    def bonus_damage_resistance(self) -> float: ...
    @bonus_damage_resistance.setter
    def bonus_damage_resistance(self, value: float) -> None: ...

    @property
    def break_off_combat(self) -> int: ...
    @break_off_combat.setter
    def break_off_combat(self, value: int) -> None: ...

    @property
    def damage_reflection(self) -> float: ...
    @damage_reflection.setter
    def damage_reflection(self, value: float) -> None: ...

    @property
    def defense_terrain_bonus(self) -> int: ...
    @defense_terrain_bonus.setter
    def defense_terrain_bonus(self, value: int) -> None: ...

    @property
    def displayed_attack(self) -> int: ...
    @displayed_attack.setter
    def displayed_attack(self, value: int) -> None: ...

    @property
    def displayed_melee_armour(self) -> int: ...
    @displayed_melee_armour.setter
    def displayed_melee_armour(self, value: int) -> None: ...

    @property
    def displayed_range(self) -> float: ...
    @displayed_range.setter
    def displayed_range(self, value: float) -> None: ...

    @property
    def displayed_reload_time(self) -> float: ...
    @displayed_reload_time.setter
    def displayed_reload_time(self, value: float) -> None: ...

    @property
    def frame_delay(self) -> int: ...
    @frame_delay.setter
    def frame_delay(self, value: int) -> None: ...

    @property
    def friendly_fire_damage(self) -> float: ...
    @friendly_fire_damage.setter
    def friendly_fire_damage(self, value: float) -> None: ...

    @property
    def garrison_firepower(self) -> float: ...
    @garrison_firepower.setter
    def garrison_firepower(self, value: float) -> None: ...

    @property
    def graphic_displacement(self) -> Tuple: ...
    @graphic_displacement.setter
    def graphic_displacement(self, value: Tuple) -> None: ...

    @property
    def interrupt_frame(self) -> int: ...
    @interrupt_frame.setter
    def interrupt_frame(self, value: int) -> None: ...

    @property
    def max_range(self) -> float: ...
    @max_range.setter
    def max_range(self, value: float) -> None: ...

    @property
    def min_range(self) -> float: ...
    @min_range.setter
    def min_range(self, value: float) -> None: ...

    @property
    def projectile_unit_id(self) -> int: ...
    @projectile_unit_id.setter
    def projectile_unit_id(self, value: int) -> None: ...

    @property
    def reload_time(self) -> float: ...
    @reload_time.setter
    def reload_time(self, value: float) -> None: ...

    @property
    def weapon_offset_x(self) -> float: ...
    @weapon_offset_x.setter
    def weapon_offset_x(self, value: float) -> None: ...

    @property
    def weapon_offset_y(self) -> float: ...
    @weapon_offset_y.setter
    def weapon_offset_y(self, value: float) -> None: ...

    @property
    def weapon_offset_z(self) -> float: ...
    @weapon_offset_z.setter
    def weapon_offset_z(self, value: float) -> None: ...


    # MovementWrapper flattened properties
    @property
    def max_yaw_per_sec_standing(self) -> float: ...
    @max_yaw_per_sec_standing.setter
    def max_yaw_per_sec_standing(self, value: float) -> None: ...

    @property
    def max_yaw_per_sec_walking(self) -> float: ...
    @max_yaw_per_sec_walking.setter
    def max_yaw_per_sec_walking(self, value: float) -> None: ...

    @property
    def max_yaw_per_second_moving(self) -> float: ...
    @max_yaw_per_second_moving.setter
    def max_yaw_per_second_moving(self, value: float) -> None: ...

    @property
    def max_yaw_per_second_stationary(self) -> float: ...
    @max_yaw_per_second_stationary.setter
    def max_yaw_per_second_stationary(self, value: float) -> None: ...

    @property
    def min_collision_size_multiplier(self) -> float: ...
    @min_collision_size_multiplier.setter
    def min_collision_size_multiplier(self, value: float) -> None: ...

    @property
    def old_move_algorithm(self) -> int: ...
    @old_move_algorithm.setter
    def old_move_algorithm(self, value: int) -> None: ...

    @property
    def old_size_class(self) -> int: ...
    @old_size_class.setter
    def old_size_class(self, value: int) -> None: ...

    @property
    def rotation_radius(self) -> float: ...
    @rotation_radius.setter
    def rotation_radius(self, value: float) -> None: ...

    @property
    def rotation_radius_speed(self) -> float: ...
    @rotation_radius_speed.setter
    def rotation_radius_speed(self, value: float) -> None: ...

    @property
    def rotation_speed(self) -> float: ...
    @rotation_speed.setter
    def rotation_speed(self, value: float) -> None: ...

    @property
    def running_graphic_id(self) -> int: ...
    @running_graphic_id.setter
    def running_graphic_id(self, value: int) -> None: ...

    @property
    def standing_yaw_revolution_time(self) -> float: ...
    @standing_yaw_revolution_time.setter
    def standing_yaw_revolution_time(self, value: float) -> None: ...

    @property
    def stationary_yaw_revolution_time(self) -> float: ...
    @stationary_yaw_revolution_time.setter
    def stationary_yaw_revolution_time(self, value: float) -> None: ...

    @property
    def tracking_unit_density(self) -> float: ...
    @tracking_unit_density.setter
    def tracking_unit_density(self, value: float) -> None: ...

    @property
    def tracking_unit_id(self) -> int: ...
    @tracking_unit_id.setter
    def tracking_unit_id(self, value: int) -> None: ...

    @property
    def tracking_unit_mode(self) -> int: ...
    @tracking_unit_mode.setter
    def tracking_unit_mode(self, value: int) -> None: ...

    @property
    def trail_mode(self) -> int: ...
    @trail_mode.setter
    def trail_mode(self, value: int) -> None: ...

    @property
    def trail_spacing(self) -> float: ...
    @trail_spacing.setter
    def trail_spacing(self, value: float) -> None: ...

    @property
    def trailing_unit_id(self) -> int: ...
    @trailing_unit_id.setter
    def trailing_unit_id(self, value: int) -> None: ...

    @property
    def turn_radius(self) -> float: ...
    @turn_radius.setter
    def turn_radius(self, value: float) -> None: ...

    @property
    def turn_radius_speed(self) -> float: ...
    @turn_radius_speed.setter
    def turn_radius_speed(self, value: float) -> None: ...

    @property
    def walking_graphic_id(self) -> int: ...
    @walking_graphic_id.setter
    def walking_graphic_id(self, value: int) -> None: ...


    # BehaviorWrapper flattened properties
    @property
    def attack_sound(self) -> int: ...
    @attack_sound.setter
    def attack_sound(self, value: int) -> None: ...

    @property
    def attack_sound_id(self) -> int: ...
    @attack_sound_id.setter
    def attack_sound_id(self, value: int) -> None: ...

    @property
    def default_task_id(self) -> int: ...
    @default_task_id.setter
    def default_task_id(self, value: int) -> None: ...

    @property
    def drop_site_unit_ids(self) -> Any: ...
    @drop_site_unit_ids.setter
    def drop_site_unit_ids(self, value: Any) -> None: ...

    @property
    def drop_sites(self) -> Any: ...
    @drop_sites.setter
    def drop_sites(self, value: Any) -> None: ...

    @property
    def move_sound(self) -> int: ...
    @move_sound.setter
    def move_sound(self, value: int) -> None: ...

    @property
    def move_sound_id(self) -> int: ...
    @move_sound_id.setter
    def move_sound_id(self, value: int) -> None: ...

    @property
    def run_mode(self) -> int: ...
    @run_mode.setter
    def run_mode(self, value: int) -> None: ...

    @property
    def run_pattern(self) -> int: ...
    @run_pattern.setter
    def run_pattern(self, value: int) -> None: ...

    @property
    def search_radius(self) -> float: ...
    @search_radius.setter
    def search_radius(self, value: float) -> None: ...

    @property
    def task_swap_group(self) -> int: ...
    @task_swap_group.setter
    def task_swap_group(self, value: int) -> None: ...

    @property
    def tasks(self) -> Any: ...
    @tasks.setter
    def tasks(self, value: Any) -> None: ...

    @property
    def work_rate(self) -> float: ...
    @work_rate.setter
    def work_rate(self, value: float) -> None: ...

    @property
    def wwise_attack_sound_id(self) -> int: ...
    @wwise_attack_sound_id.setter
    def wwise_attack_sound_id(self, value: int) -> None: ...

    @property
    def wwise_move_sound_id(self) -> int: ...
    @wwise_move_sound_id.setter
    def wwise_move_sound_id(self, value: int) -> None: ...


    # ProjectileWrapper flattened properties
    @property
    def area_effect_specials(self) -> int: ...
    @area_effect_specials.setter
    def area_effect_specials(self, value: int) -> None: ...

    @property
    def hit_mode(self) -> int: ...
    @hit_mode.setter
    def hit_mode(self, value: int) -> None: ...

    @property
    def projectile_arc(self) -> float: ...
    @projectile_arc.setter
    def projectile_arc(self, value: float) -> None: ...

    @property
    def projectile_type(self) -> int: ...
    @projectile_type.setter
    def projectile_type(self, value: int) -> None: ...

    @property
    def smart_mode(self) -> int: ...
    @smart_mode.setter
    def smart_mode(self, value: int) -> None: ...

    @property
    def vanish_mode(self) -> int: ...
    @vanish_mode.setter
    def vanish_mode(self, value: int) -> None: ...


    # CreationWrapper flattened properties
    @property
    def attack_priority(self) -> int: ...
    @attack_priority.setter
    def attack_priority(self, value: int) -> None: ...

    @property
    def button_extended_tooltip_id(self) -> int: ...
    @button_extended_tooltip_id.setter
    def button_extended_tooltip_id(self, value: int) -> None: ...

    @property
    def button_hotkey_action(self) -> int: ...
    @button_hotkey_action.setter
    def button_hotkey_action(self, value: int) -> None: ...

    @property
    def button_icon_id(self) -> int: ...
    @button_icon_id.setter
    def button_icon_id(self, value: int) -> None: ...

    @property
    def button_id(self) -> int: ...
    @button_id.setter
    def button_id(self, value: int) -> None: ...

    @property
    def button_short_tooltip_id(self) -> int: ...
    @button_short_tooltip_id.setter
    def button_short_tooltip_id(self, value: int) -> None: ...

    @property
    def charge_event(self) -> int: ...
    @charge_event.setter
    def charge_event(self, value: int) -> None: ...

    @property
    def charge_projectile_unit_id(self) -> int: ...
    @charge_projectile_unit_id.setter
    def charge_projectile_unit_id(self, value: int) -> None: ...

    @property
    def charge_target(self) -> int: ...
    @charge_target.setter
    def charge_target(self, value: int) -> None: ...

    @property
    def charge_type(self) -> int: ...
    @charge_type.setter
    def charge_type(self, value: int) -> None: ...

    @property
    def conversion_chance_mod(self) -> float: ...
    @conversion_chance_mod.setter
    def conversion_chance_mod(self, value: float) -> None: ...

    @property
    def costs(self) -> Any: ...
    @costs.setter
    def costs(self, value: Any) -> None: ...

    @property
    def creatable_type(self) -> int: ...
    @creatable_type.setter
    def creatable_type(self, value: int) -> None: ...

    @property
    def displayed_pierce_armour(self) -> int: ...
    @displayed_pierce_armour.setter
    def displayed_pierce_armour(self, value: int) -> None: ...

    @property
    def flank_attack_modifier(self) -> float: ...
    @flank_attack_modifier.setter
    def flank_attack_modifier(self, value: float) -> None: ...

    @property
    def garrison_graphic_id(self) -> int: ...
    @garrison_graphic_id.setter
    def garrison_graphic_id(self, value: int) -> None: ...

    @property
    def hero_glow_graphic_id(self) -> int: ...
    @hero_glow_graphic_id.setter
    def hero_glow_graphic_id(self, value: int) -> None: ...

    @property
    def hero_mode(self) -> int: ...
    @hero_mode.setter
    def hero_mode(self, value: int) -> None: ...

    @property
    def hot_key_id(self) -> int: ...
    @hot_key_id.setter
    def hot_key_id(self, value: int) -> None: ...

    @property
    def idle_attack_graphic_id(self) -> int: ...
    @idle_attack_graphic_id.setter
    def idle_attack_graphic_id(self, value: int) -> None: ...

    @property
    def invulnerability_level(self) -> float: ...
    @invulnerability_level.setter
    def invulnerability_level(self, value: float) -> None: ...

    @property
    def max_charge(self) -> float: ...
    @max_charge.setter
    def max_charge(self, value: float) -> None: ...

    @property
    def max_conversion_time_mod(self) -> float: ...
    @max_conversion_time_mod.setter
    def max_conversion_time_mod(self, value: float) -> None: ...

    @property
    def max_total_projectiles(self) -> int: ...
    @max_total_projectiles.setter
    def max_total_projectiles(self, value: int) -> None: ...

    @property
    def min_conversion_time_mod(self) -> float: ...
    @min_conversion_time_mod.setter
    def min_conversion_time_mod(self, value: float) -> None: ...

    @property
    def projectile_spawning_area(self) -> Tuple: ...
    @projectile_spawning_area.setter
    def projectile_spawning_area(self, value: Tuple) -> None: ...

    @property
    def projectile_spawning_area_length(self) -> float: ...
    @projectile_spawning_area_length.setter
    def projectile_spawning_area_length(self, value: float) -> None: ...

    @property
    def projectile_spawning_area_randomness(self) -> float: ...
    @projectile_spawning_area_randomness.setter
    def projectile_spawning_area_randomness(self, value: float) -> None: ...

    @property
    def projectile_spawning_area_width(self) -> float: ...
    @projectile_spawning_area_width.setter
    def projectile_spawning_area_width(self, value: float) -> None: ...

    @property
    def rear_attack_modifier(self) -> float: ...
    @rear_attack_modifier.setter
    def rear_attack_modifier(self, value: float) -> None: ...

    @property
    def recharge_rate(self) -> float: ...
    @recharge_rate.setter
    def recharge_rate(self, value: float) -> None: ...

    @property
    def resource_costs(self) -> Any: ...
    @resource_costs.setter
    def resource_costs(self, value: Any) -> None: ...

    @property
    def secondary_projectile_unit_id(self) -> int: ...
    @secondary_projectile_unit_id.setter
    def secondary_projectile_unit_id(self, value: int) -> None: ...

    @property
    def spawning_graphic_id(self) -> int: ...
    @spawning_graphic_id.setter
    def spawning_graphic_id(self, value: int) -> None: ...

    @property
    def special_ability(self) -> int: ...
    @special_ability.setter
    def special_ability(self, value: int) -> None: ...

    @property
    def special_graphic_id(self) -> int: ...
    @special_graphic_id.setter
    def special_graphic_id(self, value: int) -> None: ...

    @property
    def total_projectiles(self) -> float: ...
    @total_projectiles.setter
    def total_projectiles(self, value: float) -> None: ...

    @property
    def train_location_id(self) -> int: ...
    @train_location_id.setter
    def train_location_id(self, value: int) -> None: ...

    @property
    def train_locations(self) -> Any: ...
    @train_locations.setter
    def train_locations(self, value: Any) -> None: ...

    @property
    def train_time(self) -> int: ...
    @train_time.setter
    def train_time(self, value: int) -> None: ...

    @property
    def upgrade_graphic_id(self) -> int: ...
    @upgrade_graphic_id.setter
    def upgrade_graphic_id(self, value: int) -> None: ...


    # BuildingWrapper flattened properties
    @property
    def adjacent_mode(self) -> int: ...
    @adjacent_mode.setter
    def adjacent_mode(self, value: int) -> None: ...

    @property
    def annexes(self) -> Any: ...
    @annexes.setter
    def annexes(self, value: Any) -> None: ...

    @property
    def annexes_manager(self) -> Any: ...
    @annexes_manager.setter
    def annexes_manager(self, value: Any) -> None: ...

    @property
    def can_burn(self) -> int: ...
    @can_burn.setter
    def can_burn(self, value: int) -> None: ...

    @property
    def completion_tech_id(self) -> int: ...
    @completion_tech_id.setter
    def completion_tech_id(self, value: int) -> None: ...

    @property
    def construction_graphic_id(self) -> int: ...
    @construction_graphic_id.setter
    def construction_graphic_id(self, value: int) -> None: ...

    @property
    def construction_sound_id(self) -> int: ...
    @construction_sound_id.setter
    def construction_sound_id(self, value: int) -> None: ...

    @property
    def destruction_graphic_id(self) -> int: ...
    @destruction_graphic_id.setter
    def destruction_graphic_id(self, value: int) -> None: ...

    @property
    def destruction_rubble_graphic_id(self) -> int: ...
    @destruction_rubble_graphic_id.setter
    def destruction_rubble_graphic_id(self, value: int) -> None: ...

    @property
    def disappears_when_built(self) -> int: ...
    @disappears_when_built.setter
    def disappears_when_built(self, value: int) -> None: ...

    @property
    def foundation_terrain_id(self) -> int: ...
    @foundation_terrain_id.setter
    def foundation_terrain_id(self, value: int) -> None: ...

    @property
    def garrison_heal_rate(self) -> float: ...
    @garrison_heal_rate.setter
    def garrison_heal_rate(self, value: float) -> None: ...

    @property
    def garrison_repair_rate(self) -> float: ...
    @garrison_repair_rate.setter
    def garrison_repair_rate(self, value: float) -> None: ...

    @property
    def garrison_type(self) -> int: ...
    @garrison_type.setter
    def garrison_type(self, value: int) -> None: ...

    @property
    def graphics_angle(self) -> int: ...
    @graphics_angle.setter
    def graphics_angle(self, value: int) -> None: ...

    @property
    def head_unit_id(self) -> int: ...
    @head_unit_id.setter
    def head_unit_id(self, value: int) -> None: ...

    @property
    def looting_table(self) -> Any: ...
    @looting_table.setter
    def looting_table(self, value: Any) -> None: ...

    @property
    def old_overlap_id(self) -> int: ...
    @old_overlap_id.setter
    def old_overlap_id(self, value: int) -> None: ...

    @property
    def pile_unit_id(self) -> int: ...
    @pile_unit_id.setter
    def pile_unit_id(self, value: int) -> None: ...

    @property
    def research_complete_graphic_id(self) -> int: ...
    @research_complete_graphic_id.setter
    def research_complete_graphic_id(self, value: int) -> None: ...

    @property
    def research_graphic_id(self) -> int: ...
    @research_graphic_id.setter
    def research_graphic_id(self, value: int) -> None: ...

    @property
    def salvage_unit_id(self) -> int: ...
    @salvage_unit_id.setter
    def salvage_unit_id(self, value: int) -> None: ...

    @property
    def snow_graphic_id(self) -> int: ...
    @snow_graphic_id.setter
    def snow_graphic_id(self, value: int) -> None: ...

    @property
    def stack_unit_id(self) -> int: ...
    @stack_unit_id.setter
    def stack_unit_id(self, value: int) -> None: ...

    @property
    def tech_id(self) -> int: ...
    @tech_id.setter
    def tech_id(self, value: int) -> None: ...

    @property
    def transform_sound_id(self) -> int: ...
    @transform_sound_id.setter
    def transform_sound_id(self, value: int) -> None: ...

    @property
    def transform_unit_id(self) -> int: ...
    @transform_unit_id.setter
    def transform_unit_id(self, value: int) -> None: ...

    @property
    def wwise_construction_sound_id(self) -> int: ...
    @wwise_construction_sound_id.setter
    def wwise_construction_sound_id(self, value: int) -> None: ...

    @property
    def wwise_transform_sound_id(self) -> int: ...
    @wwise_transform_sound_id.setter
    def wwise_transform_sound_id(self, value: int) -> None: ...

