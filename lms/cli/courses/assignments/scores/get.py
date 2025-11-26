"""
Get specific scores for an assignment.
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

    assignment_query = lms.cli.common.check_required_assignment(backend, config)
    if (assignment_query is None):
        return 2

    user_queries = backend.parse_user_queries(args.users)

    scores = backend.courses_assignments_scores_get(course_query, assignment_query, user_queries)

    output = lms.model.base.base_list_to_output_format(scores, args.output_format,
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
            include_assignment = True,
    )

    parser.add_argument('users', metavar = 'USER_QUERY',
        type = str, nargs = '*',
        help = 'A query for an users to get.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
