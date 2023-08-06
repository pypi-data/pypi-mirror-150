"""Schema definitions."""
# Standard Modules
from enum import Enum

# Local Modules
from cofactr.schema.flagship.part import Part as FlagshipPart


class PartSchemaName(str, Enum):
    """Part schema name."""

    FLAGSHIP = "flagship"


schema_to_part = {PartSchemaName.FLAGSHIP: FlagshipPart}
