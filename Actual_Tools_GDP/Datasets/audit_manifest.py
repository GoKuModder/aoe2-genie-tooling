"""
Audit Manifest - Validate and generate review table from manifest.csv.

Usage:
    python audit_manifest.py

Generates manifest_review.md with a formatted table for user approval.
"""
import csv
from pathlib import Path
from typing import Dict, List, Set

# Path constants
DATASETS_DIR = Path(__file__).parent
MANIFEST_PATH = DATASETS_DIR / "manifest.csv"
REVIEW_PATH = DATASETS_DIR / "manifest_review.md"


def load_attribute_enum() -> Dict[int, str]:
    """Load Attribute enum from attributes.py."""
    from attributes import Attribute
    return {attr.value: attr.name for attr in Attribute}


def load_manifest() -> List[Dict[str, str]]:
    """Load manifest.csv and return list of rows."""
    with open(MANIFEST_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def validate_manifest(manifest: List[Dict], enum_attrs: Dict[int, str]) -> List[str]:
    """Validate manifest against Attribute enum. Returns list of issues."""
    issues = []
    manifest_ids = set()

    for row in manifest:
        attr_id = int(row['ID'])
        attr_name = row['Name']
        manifest_ids.add(attr_id)

        # Check ID exists in enum
        if attr_id not in enum_attrs:
            issues.append(f"ID {attr_id} ({attr_name}) not in Attribute enum")
        elif enum_attrs[attr_id] != attr_name:
            issues.append(f"ID {attr_id}: name mismatch - manifest='{attr_name}', enum='{enum_attrs[attr_id]}'")

        # Check Storage_Type is valid
        if row['Storage_Type'] not in ('Value', 'Reference', 'Bitmask', 'Enum'):
            issues.append(f"ID {attr_id}: invalid Storage_Type '{row['Storage_Type']}'")

        # Check Link_Target for References
        if row['Storage_Type'] == 'Reference' and row['Link_Target'] == 'None':
            issues.append(f"ID {attr_id}: Reference type but Link_Target is None")

    # Check for missing enum IDs
    for eid, ename in enum_attrs.items():
        if eid not in manifest_ids:
            issues.append(f"Enum ID {eid} ({ename}) missing from manifest")

    return issues


def generate_markdown_table(manifest: List[Dict]) -> str:
    """Generate Markdown table from manifest."""
    lines = []

    # Header
    lines.append("# Attribute Manifest Review")
    lines.append("")
    lines.append(f"**Total Attributes:** {len(manifest)}")
    lines.append("")

    # Summary by Storage_Type
    type_counts = {}
    for row in manifest:
        st = row['Storage_Type']
        type_counts[st] = type_counts.get(st, 0) + 1

    lines.append("## Summary by Storage Type")
    lines.append("")
    lines.append("| Storage Type | Count |")
    lines.append("|--------------|-------|")
    for st, count in sorted(type_counts.items()):
        lines.append(f"| {st} | {count} |")
    lines.append("")

    # Summary by Link_Target (for References)
    ref_targets = {}
    for row in manifest:
        if row['Storage_Type'] in ('Reference', 'Bitmask', 'Enum'):
            lt = row['Link_Target']
            ref_targets[lt] = ref_targets.get(lt, 0) + 1

    lines.append("## Summary by Link Target")
    lines.append("")
    lines.append("| Link Target | Count |")
    lines.append("|-------------|-------|")
    for lt, count in sorted(ref_targets.items()):
        lines.append(f"| {lt} | {count} |")
    lines.append("")

    # Full table
    lines.append("## Full Attribute Table")
    lines.append("")
    lines.append("| ID | Name | Storage | Link Target | Type | Description |")
    lines.append("|----|------|---------|-------------|------|-------------|")

    for row in manifest:
        lines.append(
            f"| {row['ID']} | {row['Name']} | {row['Storage_Type']} | "
            f"{row['Link_Target']} | {row['Data_Type']} | {row['Description']} |"
        )

    return "\n".join(lines)


def main():
    print("Loading Attribute enum...")
    enum_attrs = load_attribute_enum()
    print(f"  Found {len(enum_attrs)} attributes in enum")

    print("Loading manifest.csv...")
    manifest = load_manifest()
    print(f"  Found {len(manifest)} rows in manifest")

    print("Validating manifest...")
    issues = validate_manifest(manifest, enum_attrs)

    if issues:
        print(f"\n⚠ Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("  ✓ No validation issues")

    print("\nGenerating markdown table...")
    markdown = generate_markdown_table(manifest)

    REVIEW_PATH.write_text(markdown, encoding='utf-8')
    print(f"  ✓ Written to {REVIEW_PATH}")

    print("\nDone! Please review manifest_review.md before proceeding.")


if __name__ == "__main__":
    main()
