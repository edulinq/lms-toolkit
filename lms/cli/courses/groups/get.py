"""
Get specific group of a group set.
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

    queries = backend.parse_group_queries(args.groups)

    groups = backend.courses_groups_get(course_query, groupset_query, queries)

    output = lms.model.base.base_list_to_output_format(groups, args.output_format,
            skip_headers = args.skip_headers,
            pretty_headers = args.pretty_headers,
            include_extra_fields = args.include_extra_fields,
    )

    print(output)

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
    )

    parser.add_argument('groups', metavar = 'GROUP_QUERY',
        type = str, nargs = '*',
        help = 'A query for an group to get.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
