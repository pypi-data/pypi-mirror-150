"""Core functionality."""
# Standard Modules
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

# Local Modules
from cofactr.graph import GraphAPI
from cofactr.schema import PartSchemaName, schema_to_part


def search_parts(
    query: Optional[str] = None,
    limit: Optional[int] = 10,
    external: Optional[bool] = True,
    schema: PartSchemaName = PartSchemaName.FLAGSHIP,
):
    """Search for parts."""

    graph = GraphAPI()

    res = graph.get_products(
        query=query,
        limit=limit,
        external=external,
        schema=schema.value,
    )

    Part = schema_to_part[schema]  # pylint: disable=invalid-name

    res["data"] = [Part(**data) for data in res["data"]]

    return res


def get_part(
    id: str,
    external: Optional[bool] = True,
    schema: PartSchemaName = PartSchemaName.FLAGSHIP,
):
    """Get a part."""

    graph = GraphAPI()

    res = graph.get_product(
        id=id,
        external=external,
        schema=schema.value,
    )

    Part = schema_to_part[schema]  # pylint: disable=invalid-name

    res["data"] = Part(**res["data"]) if (res and res.get("data")) else None

    return res


def get_parts(
    ids: List[str],
    external: Optional[bool] = True,
    schema: PartSchemaName = PartSchemaName.FLAGSHIP,
):
    """Get a batch of parts.

    Note:
        Will evolve to use a batched requests. Where, for example, each request
        contains 50 part IDs.
    """
    with ThreadPoolExecutor() as executor:
        return dict(
            zip(
                ids,
                executor.map(
                    lambda cpid: get_part(cpid, external=external, schema=schema), ids
                ),
            )
        )
