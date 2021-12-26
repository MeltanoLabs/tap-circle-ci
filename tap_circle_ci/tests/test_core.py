"""Tests standard tap features using the built-in SDK tests library."""

import os

from singer_sdk.testing import get_standard_tap_tests

from tap_circle_ci.tap import TapCircleCI

SAMPLE_CONFIG = {
    "token": os.environ.get("TAP_CIRCLE_CI_TOKEN"),
    "org_slug": os.environ.get("TAP_CIRCLE_CI_ORG_SLUG"),
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapCircleCI, config=SAMPLE_CONFIG)
    for test in tests:
        test()
