"""CircleCI tap class."""

from __future__ import annotations

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.helpers._classproperty import classproperty  # noqa: PLC2701

from tap_circle_ci import streams


class TapCircleCI(Tap):
    """Singer tap for the CircleCI API."""

    name = "tap-circle-ci"
    package_name = "meltano-tap-circle-ci"

    @classproperty
    def config_jsonschema(cls):  # noqa: ANN201, N805
        """Return a list of configuration properties read by the tap."""
        return th.PropertiesList(
            th.Property(
                "token",
                th.StringType,
                required=True,
                description="Personal API Token you have generated that can be used to "
                "access the CircleCI API",
            ),
            th.Property(
                "org_slug",
                th.StringType,
                required=True,
                description=(
                    "Organization slug in the form vcs-slug/org-name. "
                    "Example: org-slug=gh/CircleCI-Public"
                ),
            ),
            th.Property(
                "base_url",
                th.StringType,
                default="https://circleci.com/api/v2",
                description="The API base URL to use for requests. Default, https://circleci.com/api/v2.",
            ),
            th.Property(
                "user_agent",
                th.StringType,
                default=f"{cls.name}/{cls.plugin_version} {cls.__doc__}",
                description="User-Agent header",
            ),
        ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        return [
            streams.JobsStream(tap=self),
            streams.PipelinesStream(tap=self),
            streams.WorkflowsStream(tap=self),
        ]
