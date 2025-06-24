import sys

import lms.api.assignment.list
import lms.cli.assignment.common
import lms.cli.common
import lms.config

DEFAULT_SKIP_DESCRIPTION = False

def run_cli(skip_description = DEFAULT_SKIP_DESCRIPTION, **kwargs):
    assignments = lms.api.assignment.list.request(**kwargs)

    keys = lms.cli.assignment.common.OUTPUT_KEYS.copy()
    if (skip_description):
        keys = keys[:-1]

    return lms.cli.common.cli_list(assignments, keys,
            collective_name = 'assignments', sort_key = 'name',
            **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'List assignments in a course.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('--skip-description', dest = 'skip_description',
        action = 'store_true', default = DEFAULT_SKIP_DESCRIPTION,
        help = 'Skip outputting the assignment description (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
