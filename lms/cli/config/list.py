"""
List the current configuration options.
"""

import argparse
import sys

import edq.cli.config.list

import lms.cli.parser

CONFIG_FIELD_SEPARATOR: str = "\t"

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    return int(edq.cli.config.list.run_cli(args))

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser and add addition flags. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_server = False,
            include_auth = False,
    )

    edq.cli.config.list.modify_parser(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
