"""
Download a quiz and write it in the Quiz Composer format.
"""

import argparse
import os
import sys

import edq.util.dirent

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

    quiz_queries = []
    if (len(args.quizzes) == 0):
        quiz_queries = [quiz.to_query() for quiz in backend.courses_quizzes_resolve_and_list(course_query)]
    else:
        quiz_queries = backend.parse_quiz_queries(args.quizzes)

    if (len(quiz_queries) == 0):
        print("Found no quizzes to download.")
        return 0

    base_dir = os.path.abspath(args.out_dir)
    for quiz_query in quiz_queries:
        quiz = backend.courses_quizzes_resolve_and_download(course_query, quiz_query)

        path = os.path.join(base_dir, quiz.get_name())
        if (os.path.exists(path)):
            if (args.force):
                edq.util.dirent.remove(path)
            else:
                print(f"Directory for quiz ('{quiz.name}') already exists, skipping write: '{path}'.")
                continue

        quiz.to_dir(path)

        print(f"Wrote quiz '{quiz.name}' to '{path}'.")

    print(f"{len(quiz_queries)} quizzes written.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
        include_course = True,
    )

    parser.add_argument('--out-dir', dest = 'out_dir',
        action = 'store', type = str, default = '.',
        help = "Where the output will be written (default: %(default)s).")

    parser.add_argument('--force', dest = 'force',
        action = 'store_true', default = False,
        help = "Delete an existing quiz output directory before writing the new content (default: %(default)s).")

    parser.add_argument('quizzes', metavar = 'QUIZ_QUERY',
        type = str, nargs = '*',
        help = "A query for a quiz to get, or leave empty to download all quizzes for the course.")

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
