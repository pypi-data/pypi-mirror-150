"""Cursor for iterating over results."""
# Standard Modules
from itertools import islice
from typing import Callable
from urllib import parse


parse_query_params = lambda url: {
    k: v[0] for k, v in parse.parse_qs(parse.urlparse(url).query).items()
}

parse_paging_data = lambda paging: {
    "previous": parse_query_params(paging["previous"]),
    "next": parse_query_params(paging["next"]),
}

first = lambda xs, i: list(islice(xs, None, i))


class Cursor(object):
    """Cursor for iterating over results."""

    def __init__(
        self,
        request: Callable,
        before,
        after,
        limit,
        batch_size,
    ):

        self.request = request
        self.limit = limit
        self.batch_size = batch_size

        self.i = 0
        self.batch_i = self.i
        self._paging = None
        self.request_batch(before=before, after=after)

    def request_batch(self, before=None, after=None):

        self.batch = self.request(
            before=before,
            after=after,
            limit=min((self.limit - self.i), self.batch_size),
        )

        batch_paging = parse_paging_data(self.batch["paging"])

        if not self._paging:
            self._paging = {"previous": batch_paging["previous"]}

    def __iter__(self):

        return self

    def __next__(self):

        if self.limit and self.i >= self.limit:
            raise StopIteration

        if self.batch is None or self.batch_i >= len(self.batch["data"]):
            next_batch = self._paging.get("next")

            if not next_batch:
                raise StopIteration

            self.batch_i = 0

            self.request_batch(
                before=next_batch.get("before"),
                after=next_batch.get("after"),
            )

        x = self.batch["data"][self.batch_i]

        self.i += 1
        self.batch_i += 1

        self._paging["next"] = {"after": x["id"], "limit": self.batch_size}

        return x

    @property
    def paging(self):

        return self._paging
