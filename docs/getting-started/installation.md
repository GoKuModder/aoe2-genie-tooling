# Installation

## Requirements

- Python 3.11 or higher
- genieutils-py (auto-installed)

## Install from PyPI

```bash
pip install aoe2-genie-tooling
```

## Install from Source

```bash
git clone https://github.com/GoKuModder/aoe2-genie-tooling.git
cd aoe2-genie-tooling
pip install -e .
```

## Development Dependencies

For contributing:

```bash
pip install -e ".[dev]"
```

This includes:
- `pytest` for testing
- `ruff` for linting

## Verify Installation

```python
from Actual_Tools import GenieWorkspace

print("aoe2-genie-tooling installed successfully!")
```
