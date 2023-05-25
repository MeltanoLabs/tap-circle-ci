"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_tap_test_class

from tap_circle_ci.tap import TapCircleCI

TestTapCircleCI = get_tap_test_class(TapCircleCI, config={})
