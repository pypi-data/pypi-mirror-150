"""Part class."""
# Standard Modules
from dataclasses import dataclass
from typing import Dict, List, Optional

# Local Modules
from cofactr.schema.flagship.offer import Offer


@dataclass
class Part:  # pylint: disable=too-many-instance-attributes
    """Part."""

    id: str
    datasheet: str
    description: str
    specs: Dict
    hero_image: str
    mpn: str
    mfr: str  # manufacturer name.
    documents: List
    msl: int
    package: Optional[str]
    terminations: Optional[int]
    updated_at: str
    buyable: int
    quotable: int
    maybe: int
    offers: List[Offer]

    def __post_init__(self):
        self.offers = [Offer(**offer) for offer in self.offers] if self.offers else []

    # def calc_overage(quant: int) -> int:
    #     return quant
