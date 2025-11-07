"""
The `lms.cli.server` package contains tools for interacting with LMS servers outside of a course/user context.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
