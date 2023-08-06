"""Cofactr graph API client."""
# Python Modules
import json
from typing import Literal, Optional

# 3rd Party Modules
import urllib3

Protocol = Literal["http", "https"]


drop_none_values = lambda d: {k: v for k, v in d.items() if v is not None}


def get_products(
    http, url, query, fields, before, after, limit, external, schema
):  # pylint: disable=too-many-arguments
    """Get products."""
    res = http.request(
        "GET",
        f"{url}/products",
        fields=drop_none_values(
            {
                "q": query,
                "fields": fields,
                "before": before,
                "after": after,
                "limit": limit,
                "external": external,
                "schema": schema,
            }
        ),
    )

    return json.loads(res.data.decode("utf-8"))


def get_orgs(
    http, url, query, before, after, limit, schema
):  # pylint: disable=too-many-arguments
    """Get orgs."""
    res = http.request(
        "GET",
        f"{url}/orgs",
        fields=drop_none_values(
            {
                "q": query,
                "before": before,
                "after": after,
                "limit": limit,
                "schema": schema,
            }
        ),
    )

    return json.loads(res.data.decode("utf-8"))


class GraphAPI:
    """A client-side representation of the Cofactr graph API."""

    PROTOCOL: Protocol = "https"
    HOST = "graph.cofactr.com"

    def __init__(
        self, protocol: Optional[Protocol] = PROTOCOL, host: Optional[str] = HOST
    ):

        self.url = f"{protocol}://{host}"
        self.http = urllib3.PoolManager()

    def check_health(self):
        """Check the operational status of the service."""

        res = self.http.request("GET", self.url)

        return json.loads(res.data.decode("utf-8"))

    def get_products(  # pylint: disable=too-many-arguments
        self,
        query: Optional[str] = None,
        fields: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        external: Optional[bool] = True,
        schema: Optional[str] = None,
    ):
        """Get products.

        Args:
            query: Search query.
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
                Example: "id,aliases,labels,statements{spec,assembly},offers"
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            external: Whether to query external sources.
            schema: Response schema.
        """

        return get_products(
            http=self.http,
            url=self.url,
            query=query,
            fields=fields,
            external=external,
            before=before,
            after=after,
            limit=limit,
            schema=schema,
        )

    def get_orgs(  # pylint: disable=too-many-arguments
        self,
        query: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        schema: Optional[str] = None,
    ):
        """Get organizations.

        Args:
            query: Search query.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            schema: Response schema.
        """

        return get_orgs(
            http=self.http,
            url=self.url,
            query=query,
            before=before,
            after=after,
            limit=limit,
            schema=schema,
        )

    def get_product(
        self,
        id: str,
        fields: Optional[str] = None,
        external: Optional[bool] = True,
        schema: Optional[str] = None,
    ):
        """Get product.

        Args:
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
                Example: "id,aliases,labels,statements{spec,assembly},offers"
            external: Whether to query external sources in order to update information for the
                given product.
            schema: Response schema.
        """

        res = self.http.request(
            "GET",
            f"{self.url}/products/{id}",
            fields=drop_none_values(
                {
                    "fields": fields,
                    "external": external,
                    "schema": schema,
                }
            ),
        )

        return json.loads(res.data.decode("utf-8"))

    def get_org(self, id: str, schema: Optional[str] = None):
        """Get organization."""

        res = self.http.request(
            "GET", f"{self.url}/orgs/{id}", fields=drop_none_values({"schema": schema})
        )

        return json.loads(res.data.decode("utf-8"))
