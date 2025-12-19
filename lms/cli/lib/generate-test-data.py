# pylint: disable=invalid-name

"""
Generate test data by starting the specified server and running all tests in this project.
"""

import argparse
import sys

import edq.testing.serverrunner

import lms.cli.parser
import lms.testing.testdata

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    return lms.testing.testdata.generate(args)

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_server = False,
            include_auth = False,
    )

    edq.testing.serverrunner.modify_parser(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
