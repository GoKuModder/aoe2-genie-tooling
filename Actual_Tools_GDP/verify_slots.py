
import sys
import os

# Set PYTHONPATH to project root
current_dir = os.getcwd()
sys.path.append(current_dir)

try:
    from Actual_Tools_GDP.Units.unit_handle import UnitHandle
    print("UnitHandle imported successfully.")
    
    # Mock workspace and unit for testing
    class MockUnit:
        def __init__(self):
            self.id = 1
            self.name = "Test"
            self.creation_info = None # For flattened checks
    
    class MockCiv:
        def __init__(self):
            self.units = [MockUnit()]
            
    class MockDat:
        def __init__(self):
            self.civilizations = [MockCiv()]
            
    class MockWorkspace:
        def __init__(self):
            self.dat = MockDat()
            
    ws = MockWorkspace()
    unit = UnitHandle(ws, 0)
    
    print(f"Testing invalid assignment on UnitHandle (slots: {len(UnitHandle.__slots__)})")
    try:
        unit.this_does_not_exist = 1
        print("FAIL: Assignment to 'this_does_not_exist' succeeded on UnitHandle!")
    except AttributeError as e:
        print(f"SUCCESS: Assignment failed as expected with AttributeError: {e}")
        
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
