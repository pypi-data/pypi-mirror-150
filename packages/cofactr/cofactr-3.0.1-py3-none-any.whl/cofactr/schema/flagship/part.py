"""Part class."""
# Standard Modules
from dataclasses import dataclass
from typing import Dict, List, Optional

# Local Modules
from cofactr.schema.types import Document


@dataclass
class Part:  # pylint: disable=too-many-instance-attributes
    """Part."""

    id: str

    description: Optional[str]
    documents: List[Document]
    hero_image: Optional[str]
    mpn: Optional[str]
    mfr: Optional[str]  # manufacturer name.
    msl: Optional[str]
    package: Optional[str]
    specs: Dict[str, str]
    terminations: Optional[int]

    inventory_level: Optional[int]
    buyable: Optional[int]
    quotable: Optional[int]
    maybe: Optional[int]
    updated_at: Optional[str]
