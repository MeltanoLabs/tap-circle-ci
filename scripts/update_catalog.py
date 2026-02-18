#!/usr/bin/env -S uv run

"""Update the catalog from the CircleCI API documentation."""

import http
import json
import logging
from pathlib import Path

import urllib3
from singer_sdk.schema.source import OpenAPISchemaNormalizer
from singer_sdk.singerlib import resolve_schema_references

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger()

OPENAPI_SPEC_URL = "https://circleci.com/api/v2/openapi.json"

# Map: stream name -> (http method, OpenAPI path)
# CircleCI API v2 might use hyphenated path parameters (e.g. {pipeline-id})
STREAM_ENDPOINTS = {
    "contexts": ("get", "/context"),
    "jobs": ("get", "/workflow/{id}/job"),
    "pipelines": ("get", "/pipeline"),
    "workflows": ("get", "/pipeline/{pipeline-id}/workflow"),
}


def download_spec(url: str) -> dict:
    """Download and parse the OpenAPI spec JSON from the given URL.

    Args:
        url: The URL to download the OpenAPI spec from.

    Returns:
        A dictionary representing the OpenAPI spec.

    Raises:
        RuntimeError: If the download fails.
    """
    logger.info("Downloading OpenAPI spec from %s", url)
    response = urllib3.request("GET", url, timeout=10)
    if response.status != http.HTTPStatus.OK:
        msg = f"Failed to download spec: HTTP {response.status}"
        raise RuntimeError(msg)
    return json.loads(response.data)


def extract_item_schema(spec: dict, method: str, path: str) -> dict:
    """Extract the JSON schema for a single item from a paginated list endpoint.

    Args:
        spec: The OpenAPI spec.
        method: The HTTP method.
        path: The path.

    Returns:
        A dictionary representing the JSON schema for a single item.
    """
    endpoint_spec = spec["paths"][path][method]
    response_ref = endpoint_spec["responses"]["200"]["content"]["application/json"]["schema"]
    list_schema = resolve_schema_references({
        **response_ref,
        "components": spec["components"],
    })

    # Paginated responses have the shape: {items: [...], next_page_token: string}
    schema = list_schema["properties"]["items"]["items"]
    return OpenAPISchemaNormalizer().preprocess_schema(schema)


def main() -> None:
    """Update the OpenAPI schema from the Circle CI API."""
    logger.info("Updating OpenAPI schema from %s", OPENAPI_SPEC_URL)
    schemas_path = Path("tap_circle_ci/schemas")

    spec = download_spec(OPENAPI_SPEC_URL)

    for stream_name, (method, path) in STREAM_ENDPOINTS.items():
        logger.info(
            "Extracting schema for '%s' (%s %s)",
            stream_name,
            method.upper(),
            path,
        )
        schema = extract_item_schema(spec, method, path)
        schema_file = schemas_path / f"{stream_name}.json"
        schema_file.write_text(json.dumps(schema, indent=2) + "\n")
        logger.info("Wrote %s", schema_file)


if __name__ == "__main__":
    main()
