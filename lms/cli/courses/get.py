"""
Get a specific course.
"""

import argparse
import sys

import lms.backend.instance
import lms.cli.parser
import lms.model.base

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    backend = lms.backend.instance.get_backend(**config)
    queries = backend.parse_course_queries(args.courses)
    courses = backend.courses_get(queries)

    output = lms.model.base.base_list_to_output_format(courses, args.output_format,
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
    )

    parser.add_argument('courses', metavar = 'COURSE_QUERY',
        type = str, nargs = '*',
        help = 'A query for a course to get.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
