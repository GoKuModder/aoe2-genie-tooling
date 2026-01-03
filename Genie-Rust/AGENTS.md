# Genie-Rust Roadmap: From Prototype to Product

This document outlines the step-by-step requirements to make this Rust implementation a full, drop-in replacement for `genieutils-py`.

## Phase 1: Save Support (CRITICAL)
**Current Status:** Read-only.
**Goal:** Enable `df.save(path)` that produces binary-identical output.

### Steps:
1.  **Implement `write_to` Traits**:
    -   Update `manual_structs.rs`: implement a `write_to<W: Write>(&self, writer: &mut W)` method for **every** struct (`Civ`, `Unit`, `Graphic`, `Sound`, etc.).
    -   Crucial: This logic must match the exact byte layout of `read_from`.
2.  **Implement Size Calculation**:
    -   To write headers (e.g., `TerrainRestriction` pointers, `Unit` pointers), we need to know the *byte size* of the data before writing it.
    -   Implement `get_size_in_bytes(&self) -> usize` for all variable-size structs.
3.  **Implement `DatFile::save`**:
    -   In `datfile.rs`, implement `save(&self, path: &str)`.
    -   Logic:
        1.  Create `flate2::write::DeflateEncoder`.
        2.  Write header (Version, TerrainRestrictions).
        3.  Calculate and write `PlayerColour` size and data.
        4.  Calculate and write `Sound` size and data.
        5.  Calculate and write `Graphic` pointers and data.
        6.  (And so on for all sections).
        7.  Finish compression and write to file.

## Phase 2: Mutability & Reference Semantics (CRITICAL for Usability)
**Current Status:** Copy semantics.
**Problem:** `df.civs[0].name = "New"` modifies a *copy* of the civ, not the one inside `DatFile`. `genieutils-py` allows direct modification.
**Goal:** Enable direct modification of the Rust data tree from Python.

### Steps:
1.  **Refactor `Vec<T>` to `Vec<Py<T>>`**:
    -   Current: `pub civs: Vec<Civ>` (Rust owns the Civs).
    -   New: `pub civs: Vec<Py<Civ>>` (Python owns the Civs, Rust holds references).
    -   This allows Python to hold a direct reference to the same object instance that is in the list.
2.  **Update `DatFile` Getter/Setters**:
    -   Ensure that accessing `df.civs` returns a Python list wrapping these references.
3.  **Validate Memory Safety**:
    -   Ensure PyO3 garbage collection interacts correctly with the Rust `DatFile` lifecycle.

## Phase 3: Validation & Optimization (Nice to Have)
**Goal:** Ensure correctness and speed.

### Steps:
1.  **Round-Trip Testing**:
    -   Write a test that does: `Load -> Save -> Load`.
    -   Assert that the file saved is identical to the file loaded (or at least semantically identical).
2.  **Parallel Loading**:
    -   Utilize `rayon` to parse loose structs (like `Graphics`) in parallel.

## Summary Checklist
- [ ] Implement `write_to` for ALL structs.
- [ ] Implement `DatFile::save`.
- [ ] Refactor to use `Py<T>` for reference semantics.
- [ ] Verify `Save -> Load` roundtrip.
