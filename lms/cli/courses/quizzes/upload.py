"""
Upload a quiz.
"""

import argparse
import sys

import quizcomp.model.quiz

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

    quiz = quizcomp.model.quiz.Quiz.from_path(args.path)

    quiz_metadata = backend.courses_quizzes_resolve_and_upload(course_query, quiz, force = args.force)

    output = lms.model.base.base_list_to_output_format([quiz_metadata], config.output_format,
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
        include_course = True,
    )

    parser.add_argument('--force', dest = 'force',
        action = 'store_true', default = False,
        help = "Delete any existing quiz with a matching name (default: %(default)s).")

    parser.add_argument('path', metavar = 'QUIZ_PATH',
        type = str,
        help = "Path to a Quiz Composer quiz (JSON file).")

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
