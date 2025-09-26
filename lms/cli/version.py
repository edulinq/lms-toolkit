"""
Get the version of the LMS Toolkit package.
"""

import argparse
import sys

import edq.core.argparser

import lms

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    print(f"v{lms.__version__}")
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> edq.core.argparser.Parser:
    """ Get the parser. """

    return edq.core.argparser.get_default_parser(__doc__.strip())

if (__name__ == '__main__'):
    sys.exit(main())
