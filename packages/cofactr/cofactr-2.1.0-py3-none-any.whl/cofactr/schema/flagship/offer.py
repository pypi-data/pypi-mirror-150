"""Part offer class."""
# Standard Modules
from dataclasses import dataclass
from typing import List, Optional

# Local Modules
from cofactr.schema.flagship.seller import Seller


@dataclass
class Offer:  # pylint: disable=too-many-instance-attributes
    """Part offer."""

    buyable: Optional[int]
    quotable: Optional[int]
    maybe: Optional[int]
    is_authorized: Optional[bool]
    seller: Seller
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
    prices: Optional[List]
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
    # 2 letter country code for current location of this part.
    # Default to distributor country.
    # ship_from_country: Optional[str]

    # Was this price originally in a different currency than USD?

    def __post_init__(self):
        self.seller = Seller(**self.seller)  # pylint: disable=not-a-mapping

    # def calculate_tariffs(quant, destination_country) -> float:
    #     return  # estimated tar

    # def is_exportable(destination_country) -> bool:
    #     return
