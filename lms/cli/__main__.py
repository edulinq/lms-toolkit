"""
The `lms.cli` package contains several packages for interacting with LMS in different ways.
Each package can be invoked to list the tools (or subpackages) it contains.
Each tool includes a help prompt that can be accessed with the `-h`/`--help` flag.
"""

import sys

import lms.util.cli

def main():
    lms.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
