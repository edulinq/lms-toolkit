import sys

import lms.api.group.listgroupings
import lms.cli.common
import lms.config

OUTPUT_KEYS = [
    ('name', 'name', 'Name'),
    ('id', 'lms_id', 'LMS ID'),
]

def run_cli(**kwargs):
    groupings = lms.api.group.listgroupings.request(**kwargs)

    return lms.cli.common.cli_list(groupings, OUTPUT_KEYS,
            collective_name = 'groupings', sort_key = 'name',
            **kwargs)

def main():
    config = lms.config.get_config(exit_on_error = True, modify_parser = _modify_parser, course = True)
    return run_cli(**config)

def _modify_parser(parser):
    parser.description = ('List groupings in a course.'
        + ' LMSs may also calls groupings ("Group Sets" or "Group Categories").'
        + ' This does not list group(ing) membership.')

    lms.cli.common.add_output_args(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
