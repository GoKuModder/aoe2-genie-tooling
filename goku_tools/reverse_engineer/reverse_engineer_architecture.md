# DAT File Reverse Engineering - Technical Implementation Plan

## Core Concept
Transform binary DAT file into Python code by:
1. Introspecting object structures
2. Identifying relationships via ID thresholds
3. Grouping related objects
4. Generating creation code
5. Generating linking code

---

## Phase 1: Attribute Introspection & Code Template Generation

### Goal
Generate complete attribute list from each manager and create a reference template for `create_*()` functions.

### Input Parameters
```python
MANAGER_TYPES = ['Unit', 'Graphic', 'Sound', 'Terrain', 'Tech']
```

### Task 1.1: Generate Complete Attribute Schema

**Process**:
```python
def introspect_manager(manager_class):
    """
    Scan manager and extract ALL attributes.
    Returns: Dictionary of {attribute_name: attribute_type}
    """
    attributes = {}
    
    # Extract all properties
    for attr in dir(manager_class):
        if not attr.startswith('_'):
            attributes[attr] = type(getattr(manager_class, attr))
    
    return attributes
```

**Output Format** (`scratch_unit_attributes.json`):
```json
{
  "Unit": {
    "simple_attributes": [
      {"name": "hit_points", "type": "int"},
      {"name": "line_of_sight", "type": "float"},
      {"name": "speed", "type": "float"},
      {"name": "name", "type": "str"},
      {"name": "unit_type", "type": "enum"},
      {"name": "unit_class", "type": "int"}
    ],
    "list_attributes": [
      {"name": "attacks", "method": "add_attack", "params": ["amount", "_class", "displayed_attack"]},
      {"name": "armors", "method": "add_armor", "params": ["amount", "_class", "displayed_armor"]},
      {"name": "tasks", "method": "add_task", "params": ["task_type", "resource_in", "resource_out", "work_value1", "work_value2"]},
      {"name": "damage_sprites", "method": "add_damage_sprite", "params": ["graphic_id", "damage_percent", "apply_mode"]},
      {"name": "train_locations", "method": "add_train_location", "params": ["unit_id"]},
      {"name": "deltas", "method": "add_delta", "params": ["graphic_id", "graphic_set", "sound_id"]}
    ],
    "id_reference_fields": [
      "default_projectile",
      "sound_move",
      "sound_attack",
      "idle_graphic_id",
      "walking_graphic_id"
    ]
  },
  "Graphic": {
    "simple_attributes": [...],
    "list_attributes": [...],
    "id_reference_fields": [...]
  },
  "Sound": {
    "simple_attributes": [...],
    "list_attributes": [...],
    "id_reference_fields": [...]
  }
}
```

### Task 1.2: Generate Reference Template

**Output** (`scratch_create_unit_template.py`):
```python
def create_unit_TEMPLATE(ws):
    """
    TEMPLATE showing ALL possible attributes.
    Generated from introspection.
    Use this as reference - actual functions will have subset of these.
    """
    unit = ws.create_unit()
    
    # === SIMPLE ATTRIBUTES (ALL from introspection) ===
    unit.hit_points = VALUE
    unit.line_of_sight = VALUE
    unit.speed = VALUE
    unit.name = "VALUE"
    unit.unit_type = VALUE  # MUST INCLUDE
    unit.unit_class = VALUE  # MUST INCLUDE
    unit.garrison_capacity = VALUE
    unit.radius_x = VALUE
    unit.radius_y = VALUE
    unit.radius_z = VALUE
    # ... [ALL other simple attributes]
    
    # === LIST ATTRIBUTES (special handlers) ===
    # Attacks
    unit.add_attack(
        amount=VALUE,
        _class=VALUE,
        displayed_attack=VALUE
    )
    
    # Armors
    unit.add_armor(
        amount=VALUE,
        _class=VALUE,
        displayed_armor=VALUE
    )
    
    # Tasks
    unit.add_task(
        task_type=VALUE,
        resource_in=VALUE,
        resource_out=VALUE,
        work_value1=VALUE,
        work_value2=VALUE
    )
    
    # Damage Sprites
    unit.add_damage_sprite(
        graphic_id=VALUE,
        damage_percent=VALUE,
        apply_mode=VALUE
    )
    
    # Train Locations
    unit.add_train_location(unit_id=VALUE)
    
    # Deltas
    unit.add_delta(
        graphic_id=VALUE,
        graphic_set=VALUE,
        sound_id=VALUE
    )
    
    # === ID REFERENCE FIELDS ===
    # These will be EITHER:
    # - Hard-coded if ID < threshold
    # - Linked in apply function if ID >= threshold
    unit.default_projectile = VALUE_OR_LINK
    unit.sound_move = VALUE_OR_LINK
    unit.sound_attack = VALUE_OR_LINK
    unit.idle_graphic_id = VALUE_OR_LINK
    # ... [ALL other reference fields]
    
    return unit
```

**Validation Checkpoint**: 
- Review template against actual DAT objects
- Ensure no attributes missing
- Verify special method signatures

---

## Phase 2: ID Threshold Configuration

### Input
```python
ID_THRESHOLDS = {
    'unit': 2382,
    'graphic': 15794,
    'sound': 715
}
```

### Rule
```
IF object_id >= threshold:
    → This is OUR VARIABLE (external link, created object)
    
IF object_id < threshold:
    → This is PLAIN DATA (hard-coded value)
```

---

## Phase 3: Relationship Discovery

### Input Files
- `field_discovery.json` - Maps which fields contain ID references
- DAT file with objects
- ID thresholds from Phase 2

### Task 3.1: Scan Objects and Build Relationship Graph

**Process**:
```python
def discover_relationships(dat_file, thresholds, field_discovery):
    """
    Scan all objects with ID >= threshold.
    Use field_discovery.json to identify which fields contain references.
    Build relationship graph.
    """
    relationships = {
        'units': {},
        'graphics': {},
        'sounds': {}
    }
    
    for unit in dat_file.units:
        if unit.id >= thresholds['unit']:
            relationships['units'][unit.id] = {
                'id': unit.id,
                'type': 'unit',
                'references': []
            }
            
            # Check each field from field_discovery
            for field in field_discovery['unit_fields']:
                value = getattr(unit, field)
                if is_valid_id(value, thresholds):
                    relationships['units'][unit.id]['references'].append({
                        'field': field,
                        'target_id': value,
                        'target_type': detect_type(value, thresholds)
                    })
    
    # Repeat for graphics and sounds
    return relationships
```

**Output Format** (`relationship_graph.json`):
```json
{
  "groups": [
    {
      "group_id": "group_arcanist",
      "objects": [
        {
          "id": 2401,
          "type": "unit",
          "name": "Arcanist",
          "links": [
            {"field": "default_projectile", "target_id": 2402, "target_type": "unit"},
            {"field": "sound_move", "target_id": 5023, "target_type": "sound"},
            {"field": "sound_attack", "target_id": 5024, "target_type": "sound"},
            {"field": "idle_graphic_id", "target_id": 15800, "target_type": "graphic"}
          ]
        },
        {
          "id": 2402,
          "type": "unit",
          "name": "Arcanist_Projectile",
          "links": [
            {"field": "projectile_graphic", "target_id": 15801, "target_type": "graphic"}
          ]
        },
        {
          "id": 5023,
          "type": "sound",
          "name": "Arcanist_Move",
          "links": []
        },
        {
          "id": 5024,
          "type": "sound",
          "name": "Arcanist_Attack",
          "links": []
        },
        {
          "id": 15800,
          "type": "graphic",
          "name": "Arcanist_Idle",
          "links": []
        },
        {
          "id": 15801,
          "type": "graphic",
          "name": "Arcanist_Projectile_Trail",
          "links": []
        }
      ]
    },
    {
      "group_id": "group_knight",
      "objects": [...]
    }
  ]
}
```

**Validation Checkpoint**:
- Output this JSON for manual review
- Verify groupings make logical sense
- Check that links are correctly identified

---

## Phase 4: Identify Independent Objects

### Task 4.1: Find Orphaned IDs

**Process**:
```python
def find_independent_objects(dat_file, thresholds, relationship_graph):
    """
    Find all IDs >= threshold that are NOT in relationship_graph.
    These are standalone objects.
    """
    independent = {
        'units': [],
        'graphics': [],
        'sounds': []
    }
    
    # Get all IDs from relationship graph
    grouped_ids = extract_all_ids_from_graph(relationship_graph)
    
    # Check all objects in DAT
    for unit in dat_file.units:
        if unit.id >= thresholds['unit'] and unit.id not in grouped_ids:
            independent['units'].append(unit.id)
    
    # Repeat for graphics and sounds
    return independent
```

**Output Format** (`independent_objects.json`):
```json
{
  "units": [2500, 2501, 2600],
  "graphics": [15900, 16000],
  "sounds": [750, 751]
}
```

---

## Phase 5: Generate Folder Structure

### Structure Based on Phase 3 & 4

```
generated_code/
├── groups/                          # From Phase 3 (related objects)
│   ├── group_arcanist/
│   │   ├── create_unit_2401.py
│   │   ├── create_unit_2402.py
│   │   ├── create_sound_5023.py
│   │   ├── create_sound_5024.py
│   │   ├── create_graphic_15800.py
│   │   ├── create_graphic_15801.py
│   │   └── apply_group_arcanist.py
│   ├── group_knight/
│   └── ...
├── independent/                     # From Phase 4 (orphaned objects)
│   ├── units/
│   │   ├── create_unit_2500.py
│   │   ├── create_unit_2501.py
│   │   └── create_unit_2600.py
│   ├── graphics/
│   │   ├── create_graphic_15900.py
│   │   └── create_graphic_16000.py
│   └── sounds/
│       ├── create_sound_750.py
│       └── create_sound_751.py
└── reverse_engineer_dat.py          # Main orchestrator
```

---

## Phase 6: Generate Code for Independent Objects

### Task 6.1: Create Functions Without Linking

**Process**:
```python
def generate_independent_object_code(object_id, object_type, dat_file, thresholds, attribute_schema):
    """
    Generate create_*() function for independent object.
    ALL attributes hard-coded (no linking needed).
    """
    obj = get_object_from_dat(object_id, object_type, dat_file)
    
    code = f"def create_{object_type}_{object_id}(ws):\n"
    code += f"    {object_type} = ws.create_{object_type}()\n\n"
    
    # Simple attributes
    for attr in attribute_schema[object_type]['simple_attributes']:
        value = getattr(obj, attr['name'])
        code += f"    {object_type}.{attr['name']} = {repr(value)}\n"
    
    # List attributes (special handlers)
    for list_attr in attribute_schema[object_type]['list_attributes']:
        for item in getattr(obj, list_attr['name']):
            params = ', '.join([f"{p}={repr(item[p])}" for p in list_attr['params']])
            code += f"    {object_type}.{list_attr['method']}({params})\n"
    
    # ID reference fields - ALL hard-coded for independent objects
    for ref_field in attribute_schema[object_type]['id_reference_fields']:
        value = getattr(obj, ref_field)
        if value < thresholds[detect_type(value)]:
            code += f"    {object_type}.{ref_field} = {value}\n"
        else:
            # Even if >= threshold, still hard-code if object is independent
            code += f"    {object_type}.{ref_field} = {value}  # external reference\n"
    
    code += f"\n    return {object_type}\n"
    return code
```

**Example Output** (`create_unit_2500.py`):
```python
def create_unit_2500(ws):
    unit = ws.create_unit()
    
    unit.hit_points = 100
    unit.line_of_sight = 6
    unit.speed = 1.2
    unit.name = "IndependentUnit"
    unit.unit_type = 70
    unit.unit_class = 15
    
    unit.add_attack(amount=10, _class=1, displayed_attack=10)
    unit.add_armor(amount=2, _class=3, displayed_armor=2)
    
    unit.default_projectile = 150  # < 2382, hard-coded
    unit.sound_move = 5500  # >= 715 but independent, external reference
    
    return unit
```

---

## Phase 7: Generate Code for Related Objects (Groups)

### Task 7.1: Create Functions with Partial Linking

**Process**:
```python
def generate_group_object_code(object_id, group_data, thresholds, attribute_schema):
    """
    Generate create_*() function for object in a group.
    - Hard-code: Attributes with ID < threshold
    - Skip: Attributes with ID >= threshold that link to objects in same group
      (these will be linked in apply function)
    """
    obj = get_object_from_dat(object_id, ...)
    obj_type = get_type(object_id)
    
    # Find which fields link to other objects in this group
    linked_fields = []
    for link in find_object_in_group(object_id, group_data)['links']:
        if link['target_id'] in group_data['objects']:
            linked_fields.append(link['field'])
    
    code = f"def create_{obj_type}_{object_id}(ws):\n"
    code += f"    {obj_type} = ws.create_{obj_type}()\n\n"
    
    # Simple attributes
    for attr in attribute_schema[obj_type]['simple_attributes']:
        value = getattr(obj, attr['name'])
        code += f"    {obj_type}.{attr['name']} = {repr(value)}\n"
    
    # List attributes
    for list_attr in attribute_schema[obj_type]['list_attributes']:
        # ... same as Phase 6
    
    # ID reference fields
    for ref_field in attribute_schema[obj_type]['id_reference_fields']:
        value = getattr(obj, ref_field)
        
        if ref_field in linked_fields:
            # Skip - will be linked in apply function
            continue
        elif value < thresholds[detect_type(value)]:
            # Hard-code with comment
            code += f"    {obj_type}.{ref_field} = {value}  # could be external\n"
        else:
            # External reference outside group
            code += f"    {obj_type}.{ref_field} = {value}  # external reference\n"
    
    code += f"\n    return {obj_type}\n"
    return code
```

**Example Output** (`create_unit_2401.py` in `group_arcanist/`):
```python
def create_unit_2401(ws):
    unit = ws.create_unit()
    
    unit.hit_points = 150
    unit.line_of_sight = 8
    unit.speed = 1.0
    unit.name = "Arcanist"
    unit.unit_type = 70
    unit.unit_class = 27
    
    unit.add_attack(amount=12, _class=1, displayed_attack=12)
    unit.add_armor(amount=1, _class=3, displayed_armor=1)
    
    # Hard-coded (< threshold)
    unit.creatable.spawning_graphic_id = 12262  # could be external
    unit.creatable.upgrade_graphic_id = 12263  # could be external
    
    # Skipped (will be linked in apply):
    # - default_projectile (-> 2402 in group)
    # - sound_move (-> 5023 in group)
    # - sound_attack (-> 5024 in group)
    # - idle_graphic_id (-> 15800 in group)
    
    return unit
```

### Task 7.2: Generate Apply Function for Each Group

**Process**:
```python
def generate_apply_function(group_data):
    """
    Generate apply_group_*() function that:
    1. Creates all objects in group
    2. Links them based on relationship graph
    """
    group_name = group_data['group_id']
    
    code = f"def apply_{group_name}(ws):\n"
    code += f'    """Create and link all objects in {group_name}."""\n\n'
    
    # Step 1: Create all objects
    code += "    # Create objects\n"
    created_vars = {}
    for obj in group_data['objects']:
        var_name = f"{obj['type']}_{obj['id']}"
        created_vars[obj['id']] = var_name
        code += f"    {var_name} = create_{obj['type']}_{obj['id']}(ws)\n"
    
    code += "\n    # Link objects\n"
    
    # Step 2: Link objects
    for obj in group_data['objects']:
        source_var = created_vars[obj['id']]
        for link in obj['links']:
            if link['target_id'] in created_vars:  # Only link if target in same group
                target_var = created_vars[link['target_id']]
                code += f"    {source_var}.{link['field']} = {target_var}\n"
    
    code += f"\n    return {created_vars[group_data['objects'][0]['id']]}\n"
    return code
```

**Example Output** (`apply_group_arcanist.py`):
```python
def apply_group_arcanist(ws):
    """Create and link all objects in group_arcanist."""
    
    # Create objects
    unit_2401 = create_unit_2401(ws)
    unit_2402 = create_unit_2402(ws)
    sound_5023 = create_sound_5023(ws)
    sound_5024 = create_sound_5024(ws)
    graphic_15800 = create_graphic_15800(ws)
    graphic_15801 = create_graphic_15801(ws)
    
    # Link objects
    unit_2401.default_projectile = unit_2402
    unit_2401.sound_move = sound_5023
    unit_2401.sound_attack = sound_5024
    unit_2401.idle_graphic_id = graphic_15800
    unit_2402.projectile_graphic = graphic_15801
    
    return unit_2401
```

---

## Phase 8: Generate Master Orchestrator

### Task 8.1: Create Main Function

**Process**:
```python
def generate_master_function(relationship_graph, independent_objects):
    """
    Generate reverse_engineer_dat() that applies everything.
    """
    code = "def reverse_engineer_dat(ws):\n"
    code += '    """Recreate entire DAT file from code."""\n\n'
    
    # Apply independent objects
    code += "    # Apply independent objects\n"
    for obj_type in ['units', 'graphics', 'sounds']:
        for obj_id in independent_objects[obj_type]:
            code += f"    create_{obj_type[:-1]}_{obj_id}(ws)\n"
    
    code += "\n    # Apply groups\n"
    for group in relationship_graph['groups']:
        code += f"    apply_{group['group_id']}(ws)\n"
    
    code += "\n    return ws\n"
    return code
```

**Example Output** (`reverse_engineer_dat.py`):
```python
def reverse_engineer_dat(ws):
    """Recreate entire DAT file from code."""
    
    # Apply independent objects
    create_unit_2500(ws)
    create_unit_2501(ws)
    create_graphic_15900(ws)
    create_sound_750(ws)
    
    # Apply groups
    apply_group_arcanist(ws)
    apply_group_knight(ws)
    apply_group_archer(ws)
    
    return ws
```

---

## Validation & Execution

### Step 1: Validate Intermediate Outputs
- Review `scratch_unit_attributes.json`
- Review `relationship_graph.json`
- Review `independent_objects.json`

### Step 2: Generate All Code
- Run Phase 6 for independent objects
- Run Phase 7 for grouped objects
- Run Phase 8 for orchestrator

### Step 3: Test Execution
```python
# Load original DAT
original_dat = load_dat_file("original.dat")

# Create workspace
ws = Workspace()

# Apply reverse engineered code
reverse_engineer_dat(ws)

# Write new DAT
ws.save("regenerated.dat")

# Compare
assert compare_dats(original_dat, "regenerated.dat")
```

---

## Critical Rules Summary

### ✅ **DO**
1. Generate attribute schema from introspection (Phase 1)
2. Use ID thresholds to determine hard-coding vs linking (Phase 2)
3. Output intermediate JSONs for validation (Phases 3-4)
4. Hard-code IDs < threshold with `# could be external` comment
5. Skip linked fields in create functions, add them in apply functions
6. Include ALL special methods (add_attack, add_armor, etc.)
7. Set unit_type and unit_class

### ❌ **DON'T**
1. Skip any attributes from introspection
2. Manually set object IDs
3. Link fields with ID < threshold
4. Create objects with `get_*()` methods