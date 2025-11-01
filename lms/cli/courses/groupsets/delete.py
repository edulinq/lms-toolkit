"""
Delete a group set.
"""

import argparse
import sys

import lms.backend.instance
import lms.cli.common
import lms.cli.parser
import lms.model.base

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    backend = lms.backend.instance.get_backend(**config)

    course_query = lms.cli.common.check_required_course(backend, config)
    if (course_query is None):
        return 1

    groupset_query = lms.cli.common.check_required_groupset(backend, config)
    if (groupset_query is None):
        return 2

    result = backend.courses_groupsets_resolve_and_delete(course_query, groupset_query)

    if (not result):
        print(f"ERROR: Could not delete group set: '{groupset_query}'.")
        return 3

    print(f"Deleted group set: '{groupset_query}'.")
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_token = True,
            include_output_format = True,
            include_course = True,
            include_groupset = True,
    )

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
