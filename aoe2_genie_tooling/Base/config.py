from enum import Enum

from bfp_rs import Version
from sections.dat_versions import DE_LATEST


class ValidationLevel(Enum):
    """Validation levels for workspace operations."""
    NO_VALIDATION = "no_validation"
    VALIDATE_NEW = "validate_new"
    VALIDATE_ALL = "validate_all"


class Config:
    """Global configuration for aoe2_genie_tooling."""
    DEFAULT_VERSION = DE_LATEST
    DEFAULT_VALIDATION = ValidationLevel.VALIDATE_NEW
