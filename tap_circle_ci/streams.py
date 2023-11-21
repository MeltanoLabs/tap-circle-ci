"""Stream type classes for tap-circle-ci."""

from __future__ import annotations

import typing as t
from pathlib import Path

from tap_circle_ci.client import CircleCIStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class PipelinesStream(CircleCIStream):
    """Define pipeline stream."""

    name = "pipelines"
    path = "/pipeline"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updated_at"
    replication_method = "INCREMENTAL"
    schema_filepath = SCHEMAS_DIR / "pipelines.json"

    def get_child_context(  # noqa: PLR6301
        self,
        record: dict,
        context: dict | None,  # noqa: ARG002
    ) -> dict:
        """Return a context dictionary for child streams."""
        return {"pipeline_id": record["id"], "project_slug": record["project_slug"]}

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization."""
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

    def get_child_context(  # noqa: PLR6301
        self,
        record: dict,
        context: dict | None,  # noqa: ARG002
    ) -> dict:
        """Return a context dictionary for child streams."""
        return {"workflow_id": record["id"]}


class JobsStream(CircleCIStream):
    """Define jobs stream."""

    parent_stream_type = WorkflowsStream
    name = "jobs"
    path = "/workflow/{workflow_id}/job"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema_filepath = SCHEMAS_DIR / "jobs.json"

    def post_process(  # noqa: PLR6301
        self,
        row: dict,
        context: dict | None = None,
    ) -> dict | None:
        """Add the Workflow ID to the row."""
        if row and context:
            row["_workflow_id"] = context["workflow_id"]
        return row
