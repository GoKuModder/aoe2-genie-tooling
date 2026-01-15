"""
Constants for RECodeGenerator.
"""

# Fields that reference other objects (to skip in individual creates, handle in apply)
# Include both _id and non-_id variants since wrappers may expose both
LINK_FIELDS = {
    # Unit -> Graphic (base unit)
    "standing_sprite_id1", "standing_sprite_id2", "dying_sprite_id", "undead_sprite_id",
    # Unit -> Sound (base unit)
    "selection_sound_id", "dying_sound_id", "train_sound_id", "damage_sound_id1",
    # Unit -> Unit (base unit)
    "dead_unit_id", "blood_unit_id",
    
    # Combat wrapper (type_50)
    "type_50.attack_graphic_id", "type_50.attack_graphic_2_id", "type_50.projectile_unit_id",
    "type_50.attacking_graphic", "type_50.attacking_graphic_2",
    
    # Movement wrapper (dead_fish)
    "dead_fish.walking_graphic_id", "dead_fish.running_graphic_id", "dead_fish.tracking_unit_id",
    "dead_fish.walking_graphic", "dead_fish.running_graphic", "dead_fish.trailing_unit_id",
    
    # Creation wrapper (creatable)
    "creatable.spawning_graphic_id", "creatable.upgrade_graphic_id", "creatable.garrison_graphic_id",
    "creatable.secondary_projectile_unit_id", "creatable.charge_projectile_unit_id",
    "creatable.special_graphic_id", "creatable.hero_glow_graphic_id", "creatable.idle_attack_graphic_id",
    
    # Behavior wrapper (bird) - both variants
    "bird.attack_sound_id", "bird.move_sound_id",
    "bird.attack_sound", "bird.move_sound",
    
    # Building wrapper
    "building.construction_graphic_id", "building.snow_graphic_id",
    "building.construction_sound_id", "building.transform_sound_id",
    "building.head_unit_id", "building.stack_unit_id", "building.pile_unit_id",
    "building.transform_unit_id", "building.salvage_unit_id",
    "building.destruction_graphic_id", "building.destruction_rubble_graphic_id",
    "building.research_graphic_id", "building.research_complete_graphic_id",
    
    # Graphic -> Sound (graphic can have sound reference)
    "sound", "sound_id",
}

# Properties to skip (internal, read-only, or not useful)
SKIP_PROPERTIES = {
    # Internal
    "_primary_unit", "_units", "_workspace", "_civ_id",
    "workspace", "manager", "handle", "sounds",
    # Collections (handled separately)
    "tasks", "attacks", "armours", "damage_graphics", "train_locations",
    "drop_sites", "annexes", "resource_costs", "costs", "deltas",
    # Wrapper instances
    "type_50", "dead_fish", "bird", "creatable", "building",
    "combat", "movement", "behavior", "creation",
    # Builder methods (return objects, not values)
    "add_task", "add_attack", "add_armour", "add_damage_graphic",
    "add_train_location", "add_drop_site", "add_annex", "add_delta",
    "new_sound", "add_cost",
    # Sub-objects
    "graphics", "stats", "visuals", "sound_files",
    # Version-sensitive properties (may not exist in all DAT versions)
    "creatable.attack_priority", "attack_priority",
    "creatable.default_building", "default_building",
    "creatable.charge_target", "charge_target",
    "creatable.charge_type", "charge_type",
    "creatable.hot_key_id", "hot_key_id",
    "creatable.train_hotkey", "train_hotkey",
    "creatable.train_location_new", "train_location_new",
    "creatable.total_projectiles", "total_projectiles",
    "creatable.can_convert", "can_convert",
    "creatable.min_conversion_time_modifier", "min_conversion_time_modifier",
    "creatable.max_conversion_time_modifier", "max_conversion_time_modifier",
    "creatable.conversion_chance_modifier", "conversion_chance_modifier",
    "creatable.invulnerability_level", "invulnerability_level",
}

# Properties that start with these prefixes should be skipped
SKIP_PREFIXES = {
    "button_",  # All button properties are version-sensitive
    "creatable.button_",
    "creatable.charge_",  # Charge properties are version-sensitive
    "charge_",
}
