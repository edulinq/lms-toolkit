"""
Shallow frontend for edq.config.cmd.list.
"""

import argparse
import sys

import edq.config.cmd.list

import lms.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    return edq.config.cmd.list.run(args)

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser and add addition flags. """

    parser = lms.cli.parser.get_parser(edq.config.cmd.list.__doc__.strip(),
        include_server = False,
        include_auth = False,
    )
    edq.config.cmd.list.modify_parser(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
