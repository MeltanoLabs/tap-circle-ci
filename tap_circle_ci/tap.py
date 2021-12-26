"""CircleCI tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.helpers._classproperty import classproperty

from tap_circle_ci.streams import JobsStream, PipelinesStream, WorkflowsStream

STREAM_TYPES = [PipelinesStream, WorkflowsStream, JobsStream]


class TapCircleCI(Tap):
    """Singer tap for the CircleCI API."""

    name = "tap-circle-ci"

    @classproperty
    def config_jsonschema(cls):
        """Return a property list with all the configuration variables
        read by the tap."""
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
                description="Organization slug in the form vcs-slug/org-name. "
                "Example: org-slug=gh/CircleCI-Public",
            ),
            th.Property(
                "base_url", th.StringType, default="https://circleci.com/api/v2"
            ),
            th.Property(
                "user_agent",
                th.StringType,
                default=f"{cls.name}/{cls.plugin_version} {cls.__doc__}",
                description="User-Agent header",
            ),
        ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
