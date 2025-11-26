"""
Add users to a group.
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

    group_query = lms.cli.common.check_required_group(backend, config)
    if (group_query is None):
        return 3

    user_queries = backend.parse_user_queries(args.users)

    count = backend.courses_groups_memberships_resolve_and_add(course_query, groupset_query, group_query, user_queries)

    print(f"Added {count} users to group {group_query}.")

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
    )

    parser.add_argument('users', metavar = 'USER_QUERY',
        type = str, nargs = '+',
        help = 'A query for a user to add to the group.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
