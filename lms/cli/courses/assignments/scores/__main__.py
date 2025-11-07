"""
The `lms.cli.courses.assignments.scores` package contains tools for interacting with LMS course assignment scores.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
