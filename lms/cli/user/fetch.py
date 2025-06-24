import sys

import lms.api.user.fetch
import lms.cli.common
import lms.cli.user.common
import lms.config

DEFAULT_INCLUDE_ROLE = False

def run_cli(user = None, include_role = DEFAULT_INCLUDE_ROLE, **kwargs):
    raw_users = []
    if (user is not None):
        raw_users.append(user)

    users = lms.api.user.fetch.request(users = raw_users, include_role = include_role,
            **kwargs)

    keys = lms.cli.user.common.OUTPUT_KEYS.copy()
    if (include_role):
        keys.append(lms.cli.user.common.ENROLLMENT_KEY)

    return lms.cli.common.cli_list(users, keys,
            collective_name = 'user', sort_key = 'email',
            **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'Fetch information for a user.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('--include-role', dest = 'include_role',
        action = 'store_true', default = DEFAULT_INCLUDE_ROLE,
        help = 'Include user\'s role in the course (default: %(default)s).')

    parser.add_argument('user',
        action = 'store', type = str,
        help = 'The query for the user to fetch information about.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
