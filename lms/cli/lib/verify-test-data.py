# pylint: disable=invalid-name

"""
Verify test data by starting the specified server and testing HTTP exchanges against it.
"""

import argparse
import sys

import lms.cli.parser
import lms.procedure.verify_test_data
import lms.procedure.server

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    return lms.procedure.verify_test_data.run(args)

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip())

    lms.procedure.server.modify_parser(parser)

    parser.add_argument('test_data_dir', metavar = 'TEST_DATA_DIR',
        action = 'store', type = str,
        help = 'The directory to search for HTTP exchanges.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
