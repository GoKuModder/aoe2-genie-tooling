"""Extract all Unit component attributes."""
import sys
sys.path.insert(0, '..')
from genieutils.unit import Unit, Bird, DeadFish, Type50, Projectile, Creatable, Building
from dataclasses import fields

print("=== UNIT ATTRIBUTES ===")
unit_fields = [f.name for f in fields(Unit)]
print(f"Unit ({len(unit_fields)} fields):")
for f in sorted(unit_fields):
    print(f"  - {f}")

print("\n=== COMPONENT ATTRIBUTES ===")
components = {
    "Bird": Bird,
    "DeadFish": DeadFish,
    "Type50": Type50,
    "Projectile": Projectile,
    "Creatable": Creatable,
    "Building": Building,
}

all_attrs = set(unit_fields)
for name, cls in components.items():
    comp_fields = [f.name for f in fields(cls)]
    all_attrs.update(comp_fields)
    print(f"\n{name} ({len(comp_fields)} fields):")
    for f in sorted(comp_fields):
        print(f"  - {f}")

print(f"\n=== TOTAL UNIQUE: {len(all_attrs)} ===")

# Load Attribute enum
from attributes import Attribute
enum_names = {a.name.lower() for a in Attribute}

# Find NOT in enum
missing = []
for attr in sorted(all_attrs):
    if attr.lower() not in enum_names:
        missing.append(attr)

print(f"\n=== NOT IN ATTRIBUTE ENUM ({len(missing)} attrs) ===")
for attr in missing:
    print(f"  - {attr}")
