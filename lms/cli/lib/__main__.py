"""
The `lms.cli.lib` package contains tools for the LMS Toolkit itself (and does not interacting with any LMS).
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
