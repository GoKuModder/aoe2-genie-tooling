"""Type stubs for DeltaHandle - enables IDE autocomplete"""

class DeltaHandle:
    """Handle for a single delta (sub-graphic attachment)."""
    
    @property
    def delta_id(self) -> int:
        """Get the delta index."""
        ...
    
    @property
    def graphic_id(self) -> int:
        """Get/set the referenced graphic ID."""
        ...
    
    @graphic_id.setter
    def graphic_id(self, value: int) -> None: ...
    
    @property
    def offset_x(self) -> int:
        """Get/set X offset from parent."""
        ...
    
    @offset_x.setter
    def offset_x(self, value: int) -> None: ...
    
    @property
    def offset_y(self) -> int:
        """Get/set Y offset from parent."""
        ...
    
    @offset_y.setter
    def offset_y(self, value: int) -> None: ...
    
    @property
    def display_angle(self) -> int:
        """Get/set display angle filter (-1 = all angles)."""
        ...
    
    @display_angle.setter
    def display_angle(self, value: int) -> None: ...
