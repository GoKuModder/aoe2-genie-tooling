# AGENTS.md: Actual_Tools Directory

This document provides guidance for AI agents working within the `Actual_Tools/` directory.

## Purpose

The `Actual_Tools/` directory contains the high-level Python interface for interacting with the Genie Engine data files. It acts as a wrapper around the Rust backend (`Genie-Rust/`) and provides user-facing tools, APIs, and data manipulation scripts.

The primary goal of this directory is to provide a user-friendly and Pythonic way to read, modify, and write `.dat` files for Age of Empires II.

## Key Files and Directories

- **`backend.py`**: This is the abstraction layer that loads the core data classes (like `DatFile`, `Unit`, `Civ`) from either the Rust backend (`genie_rust`) or the pure Python fallback (`genieutils`). This file is critical for keeping the rest of the codebase backend-agnostic.

- **`run_tools.py` / `run_tools_user.py`**: These are the main entry points for executing command-line tools and scripts that perform operations on the data files.

- **`Base/`**: Contains base classes and data structures that are inherited or used by other modules in the directory.

- **`Units/`, `Civilizations/`, `Techs/`, `Effects/`, `Graphics/`, `Sounds/`**: These directories contain modules and classes that represent the various data structures within the Genie Engine. For example, `Units/` would contain logic related to individual units, while `Civilizations/` would handle civilization-specific data.

- **`tests/`**: This directory contains the test suite for the Python toolkit. All tests for the functionality within `Actual_Tools/` should be placed here.

## Agent Instructions

1.  **Backend Abstraction**: When adding new functionality, interact with the data through the classes exposed in `backend.py`. Avoid directly importing from `genie_rust` or `genieutils` unless absolutely necessary.
2.  **High-Level Logic**: This directory is for high-level data manipulation and user-facing tools. Performance-critical, low-level parsing logic should be implemented in the `Genie-Rust/` backend.
3.  **Testing**: Any new feature or bug fix must be accompanied by relevant tests in the `tests/` directory. Use `pytest` to run the tests.
