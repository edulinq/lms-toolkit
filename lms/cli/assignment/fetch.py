import sys

import lms.api.assignment.fetch
import lms.cli.assignment.common
import lms.cli.common
import lms.config

DEFAULT_SKIP_DESCRIPTION = False

def run_cli(assignment = None, skip_description = DEFAULT_SKIP_DESCRIPTION, **kwargs):
    raw_assignments = []
    if (assignment is not None):
        raw_assignments.append(assignment)

    assignments = lms.api.assignment.fetch.request(assignments = raw_assignments, **kwargs)

    keys = lms.cli.assignment.common.OUTPUT_KEYS.copy()
    if (skip_description):
        keys = keys[:-1]

    return lms.cli.common.cli_list(assignments, keys,
            collective_name = 'assignment', sort_key = 'name',
            **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'Fetch information for an assignment.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('--skip-description', dest = 'skip_description',
        action = 'store_true', default = DEFAULT_SKIP_DESCRIPTION,
        help = 'Skip outputting the assignment description (default: %(default)s).')

    parser.add_argument('assignment',
        action = 'store', type = str,
        help = 'The query for the assignment to fetch information about.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
