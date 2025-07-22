import sys

import lms.api.quiz.list
import lms.cli.common
import lms.config

def run_cli(**kwargs):
    quizzes = lms.api.quiz.list.request(**kwargs)

    return lms.cli.common.cli_list(quizzes, collective_name = 'quizzes',
            sort_key = 'id', **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'List quizzes in a course.'

    lms.cli.common.add_output_args(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
