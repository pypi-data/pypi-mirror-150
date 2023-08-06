"""Schema definitions."""
# Standard Modules
from enum import Enum

# Local Modules
from cofactr.helpers import identity
from cofactr.schema.flagship.offer import Offer as FlagshipOffer
from cofactr.schema.logistics.offer import Offer as LogisticsOffer
from cofactr.schema.flagship.part import Part as FlagshipPart
from cofactr.schema.logistics.part import Part as LogisticsPart


class PartSchemaName(str, Enum):
    """Part schema name."""

    INTERNAL = "internal"
    FLAGSHIP = "flagship"
    LOGISTICS = "logistics"


schema_to_part = {
    PartSchemaName.INTERNAL: identity,
    PartSchemaName.FLAGSHIP: FlagshipPart,
    PartSchemaName.LOGISTICS: LogisticsPart,
}


class OffersSchemaName(str, Enum):
    """Offers schema name."""

    INTERNAL = "internal"
    FLAGSHIP = "flagship"
    LOGISTICS = "logistics"


schema_to_offers = {
    OffersSchemaName.INTERNAL: identity,
    OffersSchemaName.FLAGSHIP: lambda offers: [
        FlagshipOffer(**offer) for offer in offers
    ],
    OffersSchemaName.LOGISTICS: lambda offers: [
        LogisticsOffer(**offer) for offer in offers
    ],
}
