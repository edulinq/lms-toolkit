"""
Get the version of the LMS Toolkit package.
"""

import argparse
import sys

import lms
import lms.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    print(f"v{lms.__version__}")
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    args, _ = _get_parser().parse_known_args()
    return run_cli(args)

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    return lms.cli.parser.get_parser(__doc__.strip(),
            include_server = False,
            include_auth = False,
    )

if (__name__ == '__main__'):
    sys.exit(main())
