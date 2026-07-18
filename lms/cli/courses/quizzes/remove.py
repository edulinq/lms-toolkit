"""
Remove a quiz.
"""

import argparse
import sys

import lms.backend.instance
import lms.cli.common
import lms.cli.parser
import lms.model.base

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config
    backend = lms.backend.instance.get_backend(config)

    course_query = lms.cli.common.check_required_course(backend, config)
    if (course_query is None):
        return 1

    queries = backend.parse_assignment_queries(args.quizzes)

    removed_quizzes = backend.courses_quizzes_resolve_and_remove(course_query, queries)

    if (len(removed_quizzes) == 0):
        print('Found no quizzes to remove.')
        return 0

    for removed_quiz in removed_quizzes:
        print(f"Removed quiz: '{removed_quiz.to_query()}'.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_course = True,
    )

    parser.add_argument('quizzes', metavar = 'QUIZ_QUERY',
        type = str, nargs = '*',
        help = 'A query for a quiz to get.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
