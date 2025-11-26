"""
Get specific entries in a course's gradebook.
"""

import argparse
import sys

import lms.backend.instance
import lms.cli.common
import lms.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    backend = lms.backend.instance.get_backend(**config)

    course_query = lms.cli.common.check_required_course(backend, config)
    if (course_query is None):
        return 1

    assignment_queries = backend.parse_assignment_queries(args.assignments)
    user_queries = backend.parse_user_queries(args.users)

    gradebook = backend.courses_gradebook_get(course_query, assignment_queries, user_queries)

    output = lms.model.base.base_list_to_output_format([gradebook], args.output_format,
            skip_headers = args.skip_headers,
            pretty_headers = args.pretty_headers,
            include_extra_fields = args.include_extra_fields,
            extract_single_list = True,
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
    )

    parser.add_argument('--assignment', dest = 'assignments',
        action = 'append', type = str, default = [],
        help = 'Include this assignment in the gradebook (all assignments are included if this option is not specified).')

    parser.add_argument('--user', dest = 'users',
        action = 'append', type = str, default = [],
        help = 'Include this user in the gradebook (all users are included if this option is not specified).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
