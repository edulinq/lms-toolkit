import sys

import lms.api.quiz.fetch
import lms.cli.common
import lms.config

def run_cli(quiz = None, **kwargs):
    quiz_queries = []
    if (quiz is not None):
        quiz_queries.append(quiz)

    quizzes = lms.api.quiz.fetch.request(quizzes = quiz_queries, **kwargs)

    return lms.cli.common.cli_list(quizzes, collective_name = 'quizzes',
            sort_key = 'id', **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'Fetch a specific quiz.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('quiz',
        action = 'store', type = str,
        help = 'The query for the quiz to fetch information about.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
