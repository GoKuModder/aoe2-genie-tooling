"""
Extract all attributes from genieutils Unit class hierarchy.

This script inspects the Unit, Bird, DeadFish, Type50, Projectile,
Creatable, and Building dataclasses to find all attributes.
"""
import csv
from dataclasses import fields
from pathlib import Path
from typing import Dict, List, Set

# Import genieutils types
from genieutils.unit import Unit, Bird, DeadFish, Type50, Projectile, Creatable, Building

# Import our Attribute enum
import sys
sys.path.insert(0, str(Path(__file__).parent))
from attributes import Attribute


def get_all_unit_attributes() -> Dict[str, List[str]]:
    """Extract all attributes from Unit and its components."""
    result = {}

    # Main Unit class
    result["Unit"] = [f.name for f in fields(Unit)]

    # Component classes
    component_classes = {
        "Bird": Bird,
        "DeadFish": DeadFish,
        "Type50": Type50,
        "Projectile": Projectile,
        "Creatable": Creatable,
        "Building": Building,
    }

    for name, cls in component_classes.items():
        try:
            result[name] = [f.name for f in fields(cls)]
        except TypeError:
            # Not a dataclass
            result[name] = dir(cls)

    return result


def get_manifest_attribute_names() -> Set[str]:
    """Get attribute names from Attribute enum."""
    return {attr.name.lower() for attr in Attribute}


def main():
    print("=" * 70)
    print("GENIEUTILS UNIT ATTRIBUTES VS MANIFEST COMPARISON")
    print("=" * 70)
    print()

    # Get all unit attributes
    print("Extracting attributes from genieutils Unit classes...")
    unit_attrs = get_all_unit_attributes()

    # Get manifest attribute names (lowercase for comparison)
    manifest_names = get_manifest_attribute_names()

    # Track all unique attribute names
    all_attrs: Set[str] = set()

    # Print each component
    for component, attrs in unit_attrs.items():
        print(f"\n### {component} ({len(attrs)} attributes)")
        print("-" * 40)
        for attr in sorted(attrs):
            if not attr.startswith('_'):
                all_attrs.add(attr)
                # Check if in manifest
                in_manifest = attr.upper() in {a.name for a in Attribute}
                marker = "✓" if in_manifest else "✗ NOT IN MANIFEST"
                print(f"  {attr}: {marker}")

    # Summary
    print("\n" + "=" * 70)
    print("ATTRIBUTES NOT IN MANIFEST (need review)")
    print("=" * 70)

    missing = []
    for attr in sorted(all_attrs):
        if attr.upper() not in {a.name for a in Attribute}:
            missing.append(attr)

    for attr in missing:
        print(f"  - {attr}")

    print(f"\nTotal unit attributes: {len(all_attrs)}")
    print(f"In manifest: {len(all_attrs) - len(missing)}")
    print(f"NOT in manifest: {len(missing)}")

    # Write to file for review
    output_path = Path(__file__).parent / "unit_vs_manifest_comparison.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Unit Attributes vs Manifest Comparison\n\n")
        f.write(f"**Total unique attributes:** {len(all_attrs)}\n")
        f.write(f"**In manifest:** {len(all_attrs) - len(missing)}\n")
        f.write(f"**NOT in manifest:** {len(missing)}\n\n")

        f.write("## Attributes NOT in Manifest (need review)\n\n")
        f.write("| Attribute | Source Component |\n")
        f.write("|-----------|------------------|\n")
        for attr in missing:
            sources = [comp for comp, attrs in unit_attrs.items() if attr in attrs]
            f.write(f"| `{attr}` | {', '.join(sources)} |\n")

        f.write("\n## All Attributes by Component\n\n")
        for component, attrs in unit_attrs.items():
            f.write(f"### {component}\n\n")
            for attr in sorted(attrs):
                if not attr.startswith('_'):
                    in_manifest = attr.upper() in {a.name for a in Attribute}
                    marker = "✓" if in_manifest else "❌"
                    f.write(f"- {marker} `{attr}`\n")
            f.write("\n")

    print(f"\nWritten to: {output_path}")


if __name__ == "__main__":
    main()
