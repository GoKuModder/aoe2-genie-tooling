"""Type stubs for ResourceAccessor - enables IDE autocomplete"""
from typing import Optional

class ResourceAccessor:
    """
    Accessor for per-civilization resource values.
    
    Note: To add/remove resources globally, use CivManager.add_resource() and
          CivManager.remove_resource() - these apply to ALL civilizations.
    """
    
    def __iter__(self) -> iter:
        """Iterate over resources."""
        ...
    
    def __len__(self) -> int:
        """Get number of resources."""
        ...

    def __getitem__(self, index: int) -> float:
        """Get resource by index."""
        ...

    def __setitem__(self, index: int, value: float) -> None:
        """Set resource by index."""
        ...

    def get(self, index: int) -> Optional[float]:
        """Get a resource value by index."""
        ...

    def set(self, index: int, value: float) -> bool:
        """
        Set a resource value by index.
        
        Args:
            index: Resource index
            value: New value
            
        Returns:
            True if set, False if index out of range
        """
        ...
