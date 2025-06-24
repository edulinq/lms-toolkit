"""
The `lms.cli.assignment` package contains tools for interacting with LMS assignments.
"""

import sys

import lms.config
import lms.util.cli

def main():
    lms.util.cli.auto_list(default_parser = lms.config.get_argument_parser())
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
