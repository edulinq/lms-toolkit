"""
Attempt to identify the backend of the target server.
"""

import argparse
import sys

import lms
import lms.backend.instance
import lms.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    backend_type = lms.backend.instance.guess_backend_type(**config)
    if (backend_type is None):
        print(f"ERROR: Unable to determine backend type from server '{config.get('server', '')}'.")
        return 1

    print(backend_type)
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    return lms.cli.parser.get_parser(__doc__.strip())

if (__name__ == '__main__'):
    sys.exit(main())
