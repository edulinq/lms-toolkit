# pylint: disable=invalid-name

"""
Add a comment to an assignment submission without changing its score.
"""

import argparse
import sys

import lms.backend.instance
import lms.cli.common
import lms.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config
    backend = lms.backend.instance.get_backend(config)

    course_query = lms.cli.common.check_required_course(backend, config)
    if (course_query is None):
        return 1

    assignment_query = lms.cli.common.check_required_assignment(backend, config)
    if (assignment_query is None):
        return 2

    user_query = lms.cli.common.check_required_user(backend, config)
    if (user_query is None):
        return 3

    result = backend.courses_assignments_scores_comments_resolve_and_add(course_query, assignment_query, user_query, args.comment)
    if (not result):
        print(f"ERROR: Could not add comment for user: '{user_query}'.")
        return 4

    print(f"Added comment for user: '{user_query}'.")
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_course = True,
            include_assignment = True,
            include_user = True,
    )
    parser.add_argument('comment', metavar = 'COMMENT',
        action = 'store', type = str,
        help = 'Comment to add without changing the existing score.')
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
