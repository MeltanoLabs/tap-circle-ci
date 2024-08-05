"""Stream type classes for tap-circle-ci."""

from __future__ import annotations

import sys
import typing as t
from pathlib import Path

from tap_circle_ci.client import CircleCIStream

if sys.version_info < (3, 12):
    from typing_extensions import override
else:
    from typing import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class PipelinesStream(CircleCIStream):
    """Define pipeline stream."""

    name = "pipelines"
    path = "/pipeline"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updated_at"
    replication_method = "INCREMENTAL"
    schema_filepath = SCHEMAS_DIR / "pipelines.json"

    @override
    def get_child_context(self, record: dict, context: Context | None) -> dict:
        """Return a context dictionary for child streams.

        Returns:
            A dictionary with the context values.
        """
        return {"pipeline_id": record["id"], "project_slug": record["project_slug"]}

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Returns:
            A dictionary with the URL parameters.
        """
        params = super().get_url_params(context, next_page_token)
        params["org-slug"] = self.config.get("org_slug")
        return params


class WorkflowsStream(CircleCIStream):
    """Define workflow stream."""

    parent_stream_type = PipelinesStream
    name = "workflows"
    path = "/pipeline/{pipeline_id}/workflow"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema_filepath = SCHEMAS_DIR / "workflows.json"

    @override
    def get_child_context(self, record: dict, context: Context | None) -> dict:
        """Return a context dictionary for child streams.

        Returns:
            A dictionary with the context values.
        """
        return {"workflow_id": record["id"]}


class JobsStream(CircleCIStream):
    """Define jobs stream."""

    parent_stream_type = WorkflowsStream
    name = "jobs"
    path = "/workflow/{workflow_id}/job"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema_filepath = SCHEMAS_DIR / "jobs.json"

    @override
    def post_process(self, row: dict, context: Context | None = None) -> dict | None:
        """Add the Workflow ID to the row.

        Returns:
            The row with the transformed data.
        """
        if row and context:
            row["_workflow_id"] = context["workflow_id"]
        return row
