"""
Write quiz questions to disk in the Quiz Composer format.
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

    quiz_query = lms.cli.common.check_required_quiz(backend, config)
    if (quiz_query is None):
        return 2

    questions = []
    if (len(args.questions) == 0):
        questions = backend.courses_quizzes_questions_resolve_and_list(course_query, quiz_query)
    else:
        queries = backend.parse_quiz_question_queries(args.questions)
        questions = backend.courses_quizzes_questions_get(course_query, quiz_query, queries)

    base_dir = os.path.abspath(args.out_dir)
    for question in questions:
        path = question.write(base_dir, force = args.force)
        print(f"Wrote question '{question.name}' to '{path}'.")

    print(f"{len(questions)} questions written.")

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
        help = "Delete any existing files when writing the questions (default: %(default)s).")

    parser.add_argument('questions', metavar = 'QUESTION_QUERY',
        type = str, nargs = '*',
        help = "A query for the questions to get, or don't specity for all questions.")

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
