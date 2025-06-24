import sys

import lms.api.group.listgroupingmembership
import lms.cli.common
import lms.config

OUTPUT_KEYS = [
    ('group_name', 'group_name', 'Group Name'),
    ('lms_group_id', 'group_id', 'LMS Group ID'),
    ('email', 'email', 'Email'),
]

def run_cli(**kwargs):
    groups = lms.api.group.listgroupingmembership.request(**kwargs)

    return lms.cli.common.cli_list(groups, OUTPUT_KEYS,
            collective_name = 'groups', sort_key = 'name',
            **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = 'List the membership of all groups within a grouping.'

    lms.cli.common.add_output_args(parser)

    parser.add_argument('grouping',
        action = 'store', type = str,
        help = 'The query for the grouping (aka "group set" or "group category") to list.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
