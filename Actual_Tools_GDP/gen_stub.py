
core_attrs = {
    "id": "int", "unit_id": "int", "name": "str", "type_": "int", "enabled": "int", "disabled": "int",
    "class_": "int", "hit_points": "int", "line_of_sight": "float", "garrison_capacity": "int", "speed": "float",
    "name_str_id": "int", "creation_str_id": "int", "help_str_id": "int", "hotkey_text_str_id": "int",
    "hotkey_str_id": "int", "trait": "int", "trait_piece": "int", "standing_sprite_id1": "int",
    "standing_sprite_id2": "int", "dying_sprite_id": "int", "undead_sprite_id": "int", "icon_id": "int",
    "radius_x": "float", "radius_y": "float", "radius_z": "float", "selection_radius_x": "float",
    "selection_radius_y": "float", "selection_radius_z": "float", "selection_effect": "int",
    "editor_selection_color": "int", "train_sound_id": "int", "damage_sound_id1": "int",
    "selection_sound_id": "int", "dying_sound_id": "int", "wwise_train_sound_id": "int",
    "wwise_damage_sound_id": "int", "wwise_selection_sound_id": "int", "wwise_dying_sound_id": "int",
    "dead_unit_id": "int", "blood_unit_id": "int", "undead_mode": "int", "can_be_built_on": "int",
    "required_side_terrain_id1": "int", "required_side_terrain_id2": "int",
    "required_center_terrain_id1": "int", "required_center_terrain_id2": "int",
    "required_clearance_radius_x": "float", "required_clearance_radius_y": "float",
    "elevation_restriction_mode": "int", "terrain_restriction_id": "int", "foundation_terrain_id": "int",
    "movement_mode": "int", "obstruction_type": "int", "obstruction_class": "int",
    "resource_carry_capacity": "int", "resource_decay_rate": "float", "resource_gather_group": "int",
    "enable_auto_gather": "int", "blast_defense_level": "int", "combat_level": "int", "old_attack_mode": "int",
    "interaction_mode": "int", "minimap_mode": "int", "interface_mode": "int", "minimap_color": "int",
    "fog_visibility_mode": "int", "occlusion_mode": "int", "sort_number": "int", "hide_in_editor": "int",
    "multiple_attribute_mode": "float", "recyclable": "int", "doppelganger_mode": "int", "convert_terrain": "int"
}

building_attrs = {
    "construction_graphic_id": "int", "snow_graphic_id": "int", "destruction_graphic_id": "int",
    "destruction_rubble_graphic_id": "int", "research_graphic_id": "int", "research_complete_graphic_id": "int",
    "adjacent_mode": "int", "graphics_angle": "int", "disappears_when_built": "int", "stack_unit_id": "int",
    "old_overlap_id": "int", "tech_id": "int", "completion_tech_id": "int", "can_burn": "int",
    "head_unit_id": "int", "transform_unit_id": "int", "salvage_unit_id": "int", "pile_unit_id": "int",
    "transform_sound_id": "int", "construction_sound_id": "int", "wwise_transform_sound_id": "int",
    "wwise_construction_sound_id": "int", "garrison_type": "int", "garrison_heal_rate": "float",
    "garrison_repair_rate": "float", "looting_table": "Any", "annexes": "AnnexesManager",
    "annexes_manager": "AnnexesManager"
}

combat_attrs = {
    "attack_graphic_id": "int", "attack_graphic_2_id": "int", "max_range": "float", "min_range": "float",
    "reload_time": "float", "accuracy_percent": "int", "accuracy_dispersion": "float", "blast_width": "float",
    "blast_damage": "float", "blast_attack_level": "int", "frame_delay": "int", "break_off_combat": "int",
    "base_armor": "int", "defense_terrain_bonus": "int", "bonus_damage_resistance": "float",
    "damage_reflection": "float", "friendly_fire_damage": "float", "displayed_attack": "int",
    "displayed_melee_armour": "int", "displayed_range": "float", "displayed_reload_time": "float",
    "projectile_unit_id": "int", "graphic_displacement": "Tuple[float, float, float]",
    "weapon_offset_x": "float", "weapon_offset_y": "float", "weapon_offset_z": "float", "interrupt_frame": "int",
    "garrison_firepower": "float"
}

creation_attrs = {
    "train_time": "int", "train_location_id": "int", "button_id": "int", "hot_key_id": "int",
    "garrison_graphic_id": "int", "spawning_graphic_id": "int", "upgrade_graphic_id": "int",
    "hero_glow_graphic_id": "int", "idle_attack_graphic_id": "int", "special_graphic_id": "int",
    "max_charge": "float", "recharge_rate": "float", "charge_event": "int", "charge_type": "int",
    "charge_target": "int", "charge_projectile_unit_id": "int", "rear_attack_modifier": "float",
    "flank_attack_modifier": "float", "attack_priority": "int", "invulnerability_level": "float",
    "min_conversion_time_mod": "float", "max_conversion_time_mod": "float", "conversion_chance_mod": "float",
    "total_projectiles": "float", "max_total_projectiles": "int", "secondary_projectile_unit_id": "int",
    "projectile_spawning_area": "Tuple[float, float, float]", "projectile_spawning_area_width": "float",
    "projectile_spawning_area_length": "float", "projectile_spawning_area_randomness": "float",
    "button_icon_id": "int", "button_short_tooltip_id": "int", "button_extended_tooltip_id": "int",
    "button_hotkey_action": "int", "creatable_type": "int", "hero_mode": "int", "special_ability": "int",
    "displayed_pierce_armour": "int"
}

movement_attrs = {
    "walking_graphic_id": "int", "running_graphic_id": "int", "rotation_speed": "float", "turn_radius": "float",
    "rotation_radius": "float", "turn_radius_speed": "float", "rotation_radius_speed": "float",
    "max_yaw_per_second_moving": "float", "max_yaw_per_sec_walking": "float",
    "stationary_yaw_revolution_time": "float", "standing_yaw_revolution_time": "float",
    "max_yaw_per_second_stationary": "float", "max_yaw_per_sec_standing": "float",
    "tracking_unit_id": "int", "trailing_unit_id": "int", "tracking_unit_mode": "int", "trail_mode": "int",
    "tracking_unit_density": "float", "trail_spacing": "float", "old_size_class": "int",
    "old_move_algorithm": "int", "min_collision_size_multiplier": "float"
}

behavior_attrs = {
    "default_task_id": "int", "search_radius": "float", "work_rate": "float", "task_swap_group": "int",
    "run_mode": "int", "run_pattern": "int", "drop_site_unit_ids": "DropSitesManager", "attack_sound_id": "int",
    "attack_sound": "int", "move_sound_id": "int", "move_sound": "int", "wwise_attack_sound_id": "int",
    "wwise_move_sound_id": "int"
}

projectile_attrs = {
    "projectile_type": "int", "smart_mode": "int", "hit_mode": "int", "vanish_mode": "int",
    "area_effect_specials": "int", "projectile_arc": "float"
}

def print_props(attrs):
    for name, type_ in attrs.items():
        print(f"    @property")
        print(f"    def {name}(self) -> {type_}: ...")
        if name not in ["id", "unit_id"]: # RO
            print(f"    @{name}.setter")
            print(f"    def {name}(self, value: {type_}) -> None: ...")
        print()

print("# Core Attributes")
print_props(core_attrs)

print("# Flattened BuildingWrapper")
print_props(building_attrs)

print("# Flattened CombatWrapper")
print_props(combat_attrs)

print("# Flattened CreationWrapper")
print_props(creation_attrs)

print("# Flattened MovementWrapper")
print_props(movement_attrs)

print("# Flattened BehaviorWrapper")
print_props(behavior_attrs)

print("# Flattened ProjectileWrapper")
print_props(projectile_attrs)
