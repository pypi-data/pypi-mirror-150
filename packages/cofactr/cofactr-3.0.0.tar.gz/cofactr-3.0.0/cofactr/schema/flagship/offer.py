"""Part offer class."""
# Standard Modules
from dataclasses import dataclass
from typing import List, Literal, Optional

# Local Modules
from cofactr.kb.entity.types import PricePoint
from cofactr.schema.flagship.seller import Seller


@dataclass
class Offer:  # pylint: disable=too-many-instance-attributes
    """Part offer."""

    part: str  # Cofactr part ID.
    seller: Seller
    is_authorized: bool  # defaults to False.
    status: Optional[Literal["buyable", "quotable", "maybe"]]
    shipping_lead: Optional[int]
    # Country code for the current location of this part, defaults to
    # that of the distributor.
    ships_from_country: Optional[str]
    # Stock Keeping Unit used internally by distributor.
    sku: Optional[str]
    # The geo-political region(s) for which the offer is valid.
    eligible_region: Optional[str]
    # Number of units available to be shipped (aka Stock, Quantity).
    inventory_level: Optional[int]
    # Packaging of parts (eg Tape, Reel).
    packaging: Optional[str]
    # Minimum Order Quantity: smallest number of parts that can be
    # purchased.
    moq: Optional[int]
    prices: Optional[List[PricePoint]]
    # The URL to view offer on distributor website. This will
    # redirect via Octopart's server.
    click_url: Optional[str]
    # The last time data was fetched from external sources.
    updated_at: str
    # Number of days to acquire parts from factory.
    factory_lead_days: Optional[int]
    # Number of parts on order from factory.
    on_order_quantity: Optional[int]
    # Order multiple for factory orders.
    factory_pack_quantity: Optional[int]
    # Number of items which must be ordered together.
    order_multiple: Optional[int]
    # The quantity of parts as packaged by the seller.
    multipack_quantity: Optional[int]

    def __post_init__(self):
        self.seller = Seller(**self.seller)  # pylint: disable=not-a-mapping
