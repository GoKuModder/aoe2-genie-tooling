import inspect
import re
from pathlib import Path
from Actual_Tools_GDP.Units.unit_handle import UnitHandle

def verify_stub_matches_runtime():
    """
    Verifies that every attribute defined in unit_handle.pyi exists on the UnitHandle class at runtime.
    """
    print("Verifying UnitHandle stub against runtime implementation...")
    
    # 1. Get Runtime Attributes (properties and slots)
    runtime_attrs = set(dir(UnitHandle))
    
    # 2. Parse Stub File for declared attributes
    stub_path = Path(__file__).parent / "Units" / "unit_handle.pyi"
    if not stub_path.exists():
        print(f"Error: Could not find stub file at {stub_path}")
        return

    stub_content = stub_path.read_text()
    
    # Regex to find "attribute: type" lines
    # Excludes methods (def ...) and class/import statements
    # Simple regex: capture word at start of line followed by colon
    declared_attrs = set()
    for line in stub_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("@"):
            continue
        
        # Match "var_name: type"
        match = re.match(r"^([a-z_][a-z0-9_]*):", line)
        if match:
            declared_attrs.add(match.group(1))

    # 3. Compare
    print(f"Found {len(declared_attrs)} attributes in .pyi")
    
    missing_in_runtime = []
    for attr in declared_attrs:
        if attr not in runtime_attrs:
            missing_in_runtime.append(attr)
            
    if missing_in_runtime:
        print("\n[FAIL] The following attributes are in .pyi but NOT in .py (Runtime Error Risk!):")
        for attr in missing_in_runtime:
            print(f"  - {attr}")
    else:
        print("\n[PASS] All attributes in .pyi exist in .py")
        
    print("\n[INFO] Verification Complete.")

if __name__ == "__main__":
    verify_stub_matches_runtime()
