# Code Hierarchy

## Architecture Decision: Top-to-Bottom

**Pattern**: Dependency Injection with Workspace as Container

## GenieWorkspace Architecture

### Component Organization

**Managed Directly in GenieWorkspace:**
1. **dat_file** - The DatFile instance (from GenieDatParser)
2. **Manager Instances** - Created and owned by workspace
   - `unit_manager` - GenieUnitManager instance
   - `graphic_manager` - GraphicManager instance
   - `sound_manager` - SoundManager instance
   - `terrain_manager` - TerrainManager instance
   - `tech_manager` - TechManager instance
   - `effect_manager` - EffectManager instance
   - `civilization_manager` - CivilizationManager instance

**Separate Classes Instantiated by GenieWorkspace:**

3. **FileIO** - `FileIO()` class
   - `load(path)` - Read DAT file
   - `save(path)` - Write DAT file
   - Handles serialization/deserialization

4. **Registry** - `Registry()` class
   - Tracks all created/modified items
   - Exports JSON mapping for AoE2ScenarioParser
   - Preserves references across game patches
   - Method: `save_registry(path)` - Export JSON for ASP

5. **Validator** - `Validator()` class
   - Attribute validation (prevent typos)
   - Type checking (Sound vs Graphic IDs)
   - Object-based validation (pass Handles not ints)
   - Allow-list enforcement for flattening

6. **IDTracker** - `IDTracker()` class
   - Validates IDs are unique
   - Tracks ID moves (400 → 399)
   - Updates references automatically

7. **Logger** - `Logger()` class
   - Colored console output
   - Configurable levels (debug, info, warn, error)
   - Can be disabled

8. **Exception classes** - Module-level definitions
   - UnitIdConflictError
   - GapNotAllowedError
   - InvalidIdError
   - ValidationError
   - TemplateNotFoundError

### Initialization Flow

```python
class GenieWorkspace:
    def __init__(self, dat_file):
        # 1. Core data
        self.dat = dat_file
        
        # 2. Support systems (separate classes)
        self.file_io = FileIO(self)
        self.registry = Registry()
        self.logger = Logger()
        self.validator = Validator()
        self.id_tracker = IDTracker()
        
        # 3. Create managers (belong to workspace)
        self._unit_manager = GenieUnitManager(self)
        self._graphic_manager = GraphicManager(self)
        self._sound_manager = SoundManager(self)
        self._terrain_manager = TerrainManager(self)
        self._tech_manager = TechManager(self)
    
    @property
    def unit_manager(self):
        return self._unit_manager
    
    @classmethod
    def load(cls, path: str):
        dat_file = DatFile.from_file(path)
        return cls(dat_file)
    
    def save(self, path: str):
        self.validator.validate_all()  # Final check before save
        self.file_io.save(path)
    
    def save_registry(self, path: str):
        self.registry.export_json(path)

# Managers access dat_file through workspace
class GenieUnitManager:
    def __init__(self, workspace):
        self.workspace = workspace
    
    @property
    def dat_file(self):
        return self.workspace.dat  # Access through workspace
    
    def create(self, name, base_unit_id, **kwargs):
        # Access other managers through workspace
        unit = UnitHandle(...)
        self.workspace.registry.track("unit", name, unit.id)
        return unit
```

### User-Facing API

```python
# Load workspace
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Extract manager (property name matches class name)
unit_manager = workspace.unit_manager  # GenieUnitManager instance

# Work with manager directly
unit1 = unit_manager.create(
    name="Hero1",
    base_unit_id=4,
    unit_id=2900
)

# Flattening still works at Handle level
unit1.move_sound = 20  # Flattened from unit1.bird.move_sound
```

## Manager Naming Convention

| Property | Class | Purpose |
|----------|-------|---------|
| `workspace.unit_manager` | `GenieUnitManager` | Unit operations |
| `workspace.graphic_manager` | `GraphicManager` | Graphic operations |
| `workspace.sound_manager` | `SoundManager` | Sound operations |
| `workspace.terrain_manager` | `TerrainManager` | Terrain operations |
| `workspace.tech_manager` | `TechManager` | Tech operations |

## Benefits of Top-to-Bottom

1. **Shared Registry**: All managers can update `workspace.registry` for ASP integration.
2. **Object Validation**: `unit.graphic = graphic_handle` can verify the handle came from `workspace.graphic_manager`.
3. **Cross-Manager Access**: Unit validation can check if a graphic ID exists via `workspace.graphic_manager.exists(id)`.
4. **Single Source of Truth**: `workspace.dat` is the only DatFile instance.
5. **Intuitive Flow**: Everything starts from `workspace.load()`.

## Handle Layer (Unchanged)

Flattening happens at the Handle level, independent of architecture:

```python
class UnitHandle:
    def __getattr__(self, name):
        # Check allow-list for safety
        if name in self._flatten_map:
            component = self._flatten_map[name]
            return getattr(getattr(self._primary_unit, component), name)
        raise AttributeError(f"Unknown attribute: {name}")
```

This ensures `unit.moove_sound = 1` raises an error instead of silently creating bad state.
