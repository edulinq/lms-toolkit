import sys

import lms.api.quiz.question.list
import lms.cli.common
import lms.config

def run_cli(**kwargs):
    questions = lms.api.quiz.question.list.request(**kwargs)

    return lms.cli.common.cli_list(questions, collective_name = 'questions',
            sort_key = 'id', **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'List questions in a quiz.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('quiz',
        action = 'store', type = str,
        help = 'The query for the quiz to list questions from.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
