"""Main entrypoint of the application for debugging purposes"""

import sys
from tap_circle_ci.tap import TapCircleCI

if __name__ == '__main__':
    TapCircleCI.cli(sys.argv[1:])
