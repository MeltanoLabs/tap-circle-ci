"""REST client handling, including CircleCIStream base class."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import SchemaDirectory, StreamSchema
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import RESTStream

from tap_circle_ci import schemas

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

SCHEMAS_DIR = SchemaDirectory(schemas)


class CircleCIStream(RESTStream):
    """CircleCI stream class."""

    records_jsonpath = "$.items[*]"
    next_page_token_jsonpath = "$.next_page_token"  # noqa: S105
    schema = StreamSchema(SCHEMAS_DIR)

    @override
    @property
    def url_base(self) -> str:
        """Return the base url from the configuration."""
        return self.config["base_url"]

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator(
            key="Circle-Token",
            value=self.config["token"],
            location="header",
        )

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Returns:
            A dictionary of values to be used in URL parameterization.
        """
        params: dict = {}
        if next_page_token:
            params["page-token"] = next_page_token
        return params
