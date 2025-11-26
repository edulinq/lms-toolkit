"""
Subtract users from a group set.
"""

import argparse
import sys

import lms.backend.instance
import lms.cli.common
import lms.cli.courses.groupsets.memberships.common
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

    memberships = lms.cli.courses.groupsets.memberships.common.load_group_memberships(backend, args.path, args.skip_rows)

    counts = backend.courses_groupsets_memberships_resolve_and_subtract(course_query, groupset_query, memberships)

    for (group_query, count) in counts.items():
        print(f"Subtracted {count} users from group {group_query}.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_output_format = True,
            include_course = True,
            include_groupset = True,
            include_group = True,
            include_skip_rows = True,
    )

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where each row has 2 columns: group query and user query.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
