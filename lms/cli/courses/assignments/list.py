"""
List the assignments of a course.
"""

import argparse
import sys

import lms.backend.backend
import lms.cli.parser
import lms.model.base

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    # TEST - Adjust when new CLI changes come in.
    backend = lms.backend.backend.get_backend(**vars(args))

    assignments = backend.courses_assignments_list(args.course)
    output = lms.model.base.base_list_to_output_format(assignments, args.output_format,
            skip_headers = args.skip_headers,
            pretty_headers = args.pretty_headers,
    )

    print(output)

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    return lms.cli.parser.get_parser(__doc__.strip(),
            include_token = True,
            include_output_format = True,
            include_course = True,
    )

if (__name__ == '__main__'):
    sys.exit(main())
