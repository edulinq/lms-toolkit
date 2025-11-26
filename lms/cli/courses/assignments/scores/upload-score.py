# pylint: disable=invalid-name

"""
Upload a single score (and optional comment) for an assignment.
"""

import argparse
import sys

import lms.backend.instance
import lms.cli.common
import lms.cli.parser
import lms.model.scores

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

    user_query = lms.cli.common.check_required_user(backend, config)
    if (user_query is None):
        return 3

    scores = {
        user_query: lms.model.scores.ScoreFragment(score = args.score, comment = args.comment),
    }

    count = backend.courses_assignments_scores_resolve_and_upload(course_query, assignment_query, scores)

    print(f"Uploaded {count} Scores")

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

    parser.add_argument('score', metavar = 'SCORE',
        action = 'store', type = float,
        help = 'Score to upload.')

    parser.add_argument('comment', metavar = 'COMMENT',
        action = 'store', type = str, nargs = '?', default = None,
        help = 'Optional comment.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
