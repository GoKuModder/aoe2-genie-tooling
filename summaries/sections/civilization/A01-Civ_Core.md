# A01-Civ_Core - Civilization Core
Source modules: `GenieDatParser/src/sections/civilization/civilization.py`, `GenieDatParser/src/sections/civilization/unit_resource.py`, `GenieDatParser/src/sections/civilization/unit_damage_sprite.py`, `GenieDatParser/src/sections/civilization/type_info/damage_class.py`
Purpose: Defines the per-civilization container and the small per-unit resource/damage records used inside unit and combat definitions.
Key Objects:
- `Civilization`: The top-level civilization struct holding identity fields, per-civ resource values, and the unit table.
- `UnitResource`: A small record for unit resource amounts and storage mode.
- `UnitDamageSprite`: A small record for damage-based sprite switching.
- `DamageClass`: A small id/amount pair used for attack and armor entries.
Binary Layout Notes:
- `Civilization` uses version-specific name fields (`str16` for DE, `NtStr[20]` for older versions) combined via `RetrieverCombiner` into a single `name`.
- DE variants include a 2-byte string signature (`_str_sign_de1`, `_str_sign_de2`) immediately before the `str16` name fields.
- `num_resources` drives the repeat count for `resources` via the `resources_repeat` on-read callback; writers should keep the count aligned with list length.
- `units` is stored as `StackedAttrArray16[Option32[Unit]]`, meaning optional unit entries packed in a stacked-attribute layout.
- `UnitResource` fields are `i16 type`, `f32 quantity`, `i8 store_mode`.
- `UnitDamageSprite` fields are `i16 sprite_id`, `i16 damage_percent`, `i8 apply_mode`.
- `DamageClass` fields are `i16 id`, `i16 amount`.
Cross-Dependencies:
- `Civilization.units` depends on `sections.civilization.unit.Unit`.
- `UnitResource` and `UnitDamageSprite` are referenced by `Unit.resources` and `Unit.damage_sprites` in `unit.py`.
- `DamageClass` is referenced by `CombatInfo.attacks` and `CombatInfo.armors` in `type_info/combat_info.py`.
Integration Notes:
- `tech_tree_effect_id`, `team_bonus_effect_id`, and `unique_unit_effect_ids` link civilizations to external effect/tech tables and are version-gated.
- Version gates on `name2` and `unique_unit_effect_ids` mean tools must pass the correct `Version` to parse those fields.
Open Questions:
- The semantics of `icon_set`, `UnitResource.store_mode`, and `UnitDamageSprite.apply_mode` are not described in these modules and may be defined elsewhere.
- There is no `unit_damage.py` in this repo; `unit_damage_sprite.py` appears to be the intended damage-sprite structure.
