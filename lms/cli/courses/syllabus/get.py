"""
Get a course's syllabus.
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

    syllabus = backend.courses_syllabus_get(course_query)

    if (syllabus is None):
        print(f"<No syllabus found for course: '{course_query}'.>")
    else:
        print(syllabus)

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_course = True,
    )

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
