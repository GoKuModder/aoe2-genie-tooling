# Reference Field Discovery

Complete mapping of all reference fields across managers.

---

## Techs → `TechHandle`

| Field | Target Type |
|-------|-------------|
| `effect` | EffectId |
| `researchlocation.location` | UnitId |
| `RequiredTechs.tech` | TechId |
| `civilization` | CivId |
| `Costs.type` | ResourceId |

---

## Graphics → `GraphicHandle`

| Field | Target Type |
|-------|-------------|
| `sound` | SoundId |
| `Deltas.graphic` | GraphicId |

---

## Units → `UnitHandle`

### Graphics (21 fields)
| Field | Status |
|-------|--------|
| `standing_graphic` | ✅ |
| `special_graphic` | ✅ |
| `dying_graphic` | ✅ |
| `undead_graphic` | ✅ |
| `walking_graphic` | ✅ |
| `running_graphic` | ✅ |
| `attack_graphic` | ✅ |
| `snow_graphic` | ✅ |
| `construction_graphic` | ✅ |
| `garrison_graphic` | ⬜ |
| `destruction_graphic` | ⬜ |
| `destruction_rubble_graphic` | ⬜ |
| `attack_2_graphic` | ⬜ |
| `idle_attack_graphic` | ⬜ |
| `spawning_graphic` | ⬜ |
| `upgrade_graphic` | ⬜ |
| `hero_glow_graphic` | ⬜ |
| `researching_graphic` | ⬜ |
| `research_completed_graphic` | ⬜ |
| `DamageGraphic.graphic` | ⬜ (nested) |
| `Task.moving_graphic` | ⬜ (nested) |
| `Task.proceeding_graphic` | ⬜ (nested) |
| `Task.working_graphic` | ⬜ (nested) |
| `Task.carrying_graphic` | ⬜ (nested) |

### Sounds (10 fields)
| Field | Status |
|-------|--------|
| `selection_sound` | ✅ |
| `dying_sound` | ✅ |
| `train_sound` | ✅ |
| `damage_sound` | ✅ |
| `attack_sound` | ✅ |
| `move_sound` | ✅ |
| `construction_sound` | ✅ |
| `transform_sound` | ✅ |
| `Task.resource_gathering_sound` | ⬜ (nested) |
| `Task.deposit_sound` | ⬜ (nested) |

### Unit References (13 fields)
| Field | Status |
|-------|--------|
| `projectile_unit` | ✅ |
| `secondary_projectile_unit` | ✅ |
| `charge_projectile_unit` | ✅ |
| `dead_unit` | ✅ |
| `blood_unit` | ✅ |
| `dropsite.unit` | ⬜ (nested) |
| `trailing_unit` | ⬜ |
| `trainLocations.unit` | ⬜ (nested) |
| `stack_unit` | ⬜ |
| `head_unit` | ⬜ |
| `transform_unit` | ⬜ |
| `pile_unit` | ⬜ |
| `annex.unit` | ⬜ (nested) |

---

## Summary

| Manager | Total | Implemented | Nested |
|---------|-------|-------------|--------|
| Techs | 5 | 0 | 2 |
| Graphics | 2 | 0 | 1 |
| Units (Graphics) | 24 | 9 | 5 |
| Units (Sounds) | 10 | 8 | 2 |
| Units (UnitRefs) | 13 | 5 | 4 |
| **Total** | **54** | **22** | **14** |
