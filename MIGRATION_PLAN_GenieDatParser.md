# Migration Plan: genieutils-py → GenieDatParser

## Executive Summary

**Feasibility**: ✅ **Highly Feasible**
**Estimated Effort**: 1-3 days for core migration, 1-2 days for testing/polish.
**Risk Level**: Low - API is similar, library is actively maintained.

---

## Why GenieDatParser?

| Feature | genieutils-py | GenieDatParser |
|---------|---------------|----------------|
| Read `.dat` | ✅ | ✅ |
| **Write `.dat`** | ✅ | ✅ |
| Version Support | DE2 | AoK, AoC, HD, DE2 |
| Python Version | 3.9+ | 3.10+ |
| Dependencies | `struct`, `zlib` | `binary-file-parser`, `zlib-ng` |
| Maintainer | Community | Divy (AoE2 DE Tool Author) |
| Performance | Standard | Uses `zlib-ng` (faster) |
| Structure | Custom classes | Uses `binary-file-parser` (standardized) |

**Key Advantage**: GenieDatParser is built on `binary-file-parser`, which provides auto-generation of read/write logic. This means the codebase is cleaner, easier to extend, and less prone to manual errors. The author (Divy) is a known AoE2 modding tool developer.

---

## API Comparison

### Loading
```python
# genieutils-py
from genieutils.datfile import DatFile
dat = DatFile.parse("path/to/file.dat")

# GenieDatParser
from sections.datfile_sections import DatFile
dat = DatFile.from_file("path/to/file.dat")
```

### Saving
```python
# genieutils-py
dat.save("path/to/output.dat")

# GenieDatParser
dat.to_file("path/to/output.dat")
```

### Accessing Data
```python
# genieutils-py
unit = dat.civs[0].units[0]
unit.name  # Access field

# GenieDatParser
unit = dat.civilizations[0].units[0]
unit.name  # Access field
```

**Key Differences**:
- `civs` → `civilizations`
- `graphics` → `sprites`
- Most inner fields are the same.

---

## Step-by-Step Migration Plan

### Phase 1: Environment Setup (30 mins)
1.  **Clone Repository**:
    ```bash
    git clone https://github.com/Divy1211/GenieDatParser.git
    cd GenieDatParser
    ```
2.  **Install Dependencies**:
    ```bash
    pip install binary-file-parser>=0.3.0a15 zlib-ng>=0.5.1
    ```
3.  **Test Loading**:
    ```python
    from src.sections.datfile_sections import DatFile
    dat = DatFile.from_file(r"path/to/empires2_x2_p1.dat")
    print(len(dat.civilizations), len(dat.sprites))
    ```

### Phase 2: Adapter Layer (1-2 hours)
Create an **adapter** that provides a `genieutils-py` compatible interface over `GenieDatParser`.

**File**: `Actual_Tools/Shared/dat_adapter.py`
```python
from src.sections.datfile_sections import DatFile as _DatFile

class DatFile:
    """Adapter providing genieutils-py compatible access to GenieDatParser."""
    
    def __init__(self, _inner: _DatFile):
        self._inner = _inner

    @classmethod
    def parse(cls, path: str) -> "DatFile":
        return cls(_DatFile.from_file(path))
    
    def save(self, path: str):
        self._inner.to_file(path)

    @property
    def civs(self):
        return self._inner.civilizations

    @property
    def graphics(self):
        return self._inner.sprites
    
    # ... Add other property aliases as needed
```

### Phase 3: Manager Updates (2-4 hours)
Update existing managers (`GenieUnitManager`, `GraphicManager`, etc.) to use the adapter.

**Changes**:
-   Update `from genieutils.datfile import DatFile` → `from Actual_Tools.Shared.dat_adapter import DatFile`
-   **If field names differ** (e.g., `civ.units` vs `civ.units`): Update field access in managers.
-   **If inner struct types differ**: Update type hints.

### Phase 4: Testing (2-4 hours)
1.  **Round-Trip Test**:
    ```python
    dat = DatFile.parse("original.dat")
    dat.save("output.dat")
    # Load output.dat back, compare counts
    ```
2.  **Unit Tests**: Run existing test suites.
3.  **Manual Verification**: Open saved `.dat` in AGE (Advanced Genie Editor).

---

## Potential Issues & Mitigations

| Issue | Mitigation |
|-------|------------|
| Field name differences | Create an adapter layer to alias fields. |
| Struct type differences | Duck-typing should handle most; add adapters if needed. |
| Python 3.10 requirement | Ensure your dev environment is 3.10+. |
| `binary-file-parser` dependency | It's a pure Python package, installs easily. |

---

## Summary Checklist

- [ ] Clone GenieDatParser
- [ ] Install dependencies (`binary-file-parser`, `zlib-ng`)
- [ ] Verify load/save works on your `.dat` file
- [ ] Create `dat_adapter.py` with genieutils-py compatible API
- [ ] Update imports in managers
- [ ] Run round-trip test
- [ ] Verify in AGE

---

## Decision: Proceed?

**Recommendation**: Yes. GenieDatParser is:
1.  Actively maintained by a known AoE2 tool author.
2.  Uses a robust binary parsing framework (`binary-file-parser`).
3.  Supports both reading AND writing.
4.  Supports multiple game versions.

The migration is straightforward because the data structures are fundamentally the same. The adapter layer will handle the minor naming differences, allowing your existing `Actual_Tools` code to work with minimal changes.
