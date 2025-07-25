import sys

import lms.api.quiz.question.fetch
import lms.cli.common
import lms.config

def run_cli(question = None, **kwargs):
    question_queries = []
    if (question is not None):
        question_queries.append(question)

    questions = lms.api.quiz.question.fetch.request(questions = question_queries, **kwargs)

    return lms.cli.common.cli_list(questions, collective_name = 'questions',
            sort_key = 'id', **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'Fetch a specific question (or questions) from a quiz.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('quiz',
        action = 'store', type = str,
        help = 'The query for the quiz to fetch a question from.')

    parser.add_argument('question',
        action = 'store', type = str,
        help = 'The query for the question to fetch information about.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
