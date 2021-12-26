"""Stream type classes for tap-circle-ci."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_circle_ci.client import CircleCIStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class PipelinesStream(CircleCIStream):
    """Define pipeline stream"""

    name = "pipelines"
    path = "/pipeline"
    primary_keys = ["id"]
    replication_key = "updated_at"
    replication_method = "INCREMENTAL"
    schema_filepath = SCHEMAS_DIR / "pipelines.json"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"pipeline_id": record["id"], "project_slug": record["project_slug"]}

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["org-slug"] = self.config.get("org_slug")
        return params


class WorkflowsStream(CircleCIStream):
    """Define workflow stream."""

    parent_stream_type = PipelinesStream
    name = "workflows"
    path = "/pipeline/{pipeline_id}/workflow"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "workflows.json"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"workflow_id": record["id"]}


class JobsStream(CircleCIStream):
    """Define jobs stream."""

    parent_stream_type = WorkflowsStream
    name = "jobs"
    path = "/workflow/{workflow_id}/job"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "jobs.json"
