"""
List the scores for an assignment.
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

    course = lms.cli.common.check_required_course(config)
    if (course is None):
        return 1

    assignment = lms.cli.common.check_required_assignment(config)
    if (assignment is None):
        return 2

    backend = lms.backend.instance.get_backend(**config)

    assignment_query = backend.parse_assignment_query(config.get('assignment', None))
    if (assignment_query is None):
        print('ERROR: Empty assignment query.')
        return 3

    scores = backend.courses_assignments_scores_resolve_and_list(course, assignment_query)

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

    return lms.cli.parser.get_parser(__doc__.strip(),
            include_token = True,
            include_output_format = True,
            include_course = True,
            include_assignment = True,
    )

if (__name__ == '__main__'):
    sys.exit(main())
