"""
Write quiz to disk in the Quiz Composer format.
"""

import argparse
import os
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

    quizzes = []
    if (len(args.quizzes) == 0):
        quizzes = backend.courses_quizzes_resolve_and_list(course_query)
    else:
        queries = backend.parse_quiz_queries(args.quizzes)
        quizzes = backend.courses_quizzes_get(course_query, queries)

    base_dir = os.path.abspath(args.out_dir)
    for quiz in quizzes:
        # Get the groups and questions for this quiz.
        groups = backend.courses_quizzes_groups_resolve_and_list(course_query, quiz.to_query())
        questions = backend.courses_quizzes_questions_resolve_and_list(course_query, quiz.to_query())

        path = quiz.write(base_dir, groups, questions, force = args.force)
        print(f"Wrote quiz '{quiz.name}' to '{path}'.")

    print(f"{len(quizzes)} quizzes written.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_course = True,
            include_quiz = True,
    )

    parser.add_argument('--out-dir', dest = 'out_dir',
        action = 'store', type = str, default = '.',
        help = "Where the output will be written (default: %(default)s).")

    parser.add_argument('--force', dest = 'force',
        action = 'store_true', default = False,
        help = "Delete any existing files when writing the quizzes (default: %(default)s).")

    parser.add_argument('quizzes', metavar = 'QUIZ_QUERY',
        type = str, nargs = '*',
        help = "A query for a quiz to get, or don't specify for all quizzes.")

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
