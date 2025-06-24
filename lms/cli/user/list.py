import sys

import lms.api.user.list
import lms.cli.common
import lms.cli.user.common
import lms.config

DEFAULT_INCLUDE_ROLE = False

def run_cli(include_role = DEFAULT_INCLUDE_ROLE, **kwargs):
    users = lms.api.user.list.request(include_role = include_role,
            **kwargs)

    keys = lms.cli.user.common.OUTPUT_KEYS.copy()
    if (include_role):
        keys.append(lms.cli.user.common.ENROLLMENT_KEY)

    return lms.cli.common.cli_list(users, keys, collective_name = 'users',
            sort_key = 'email', **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'List users in a course.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('--include-role', dest = 'include_role',
        action = 'store_true', default = DEFAULT_INCLUDE_ROLE,
        help = 'Include user\'s role in the course (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
