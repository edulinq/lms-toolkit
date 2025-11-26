"""
Get specific scores for a user.
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

    user_query = lms.cli.common.check_required_user(backend, config)
    if (user_query is None):
        return 2

    assignment_queries = backend.parse_assignment_queries(args.assignments)

    scores = backend.courses_users_scores_get(course_query, user_query, assignment_queries)

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
            include_user = True,
    )

    parser.add_argument('assignments', metavar = 'ASSIGNMENT_QUERY',
        type = str, nargs = '*',
        help = 'A query for an assignments to get.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
