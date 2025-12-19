"""
Customize an argument parser for LMS Toolkit.
"""

import argparse
import typing

import edq.core.argparser
import edq.util.net
import edq.util.reflection

import lms
import lms.model.constants
import lms.util.net

CONFIG_FILENAME: str = 'edq-lms.json'

DEFAULT_SKIP_ROWS: int = 0

_set_exchanges_clean_func: bool = True  # pylint: disable=invalid-name
"""
Whether to set the exchanges clean function when creating the parser.
This may be disabled for testing.
"""

def get_parser(description: str,
        include_server: bool = True,
        include_auth: bool = True,
        include_output_format: bool = False,
        include_course: bool = False,
        include_assignment: bool = False,
        include_user: bool = False,
        include_groupset: bool = False,
        include_group: bool = False,
        include_net: bool = True,
        include_skip_rows: bool = False,
        ) -> argparse.ArgumentParser:
    """
    Get an argument parser specialized for LMS Toolkit.
    """

    config_options = {
        'config_filename': CONFIG_FILENAME,
        'cli_arg_config_map': {
            'server': 'server',
            'backend_type': 'backend_type',
            'auth_user': 'auth_user',
            'auth_password': 'auth_password',
            'auth_token': 'auth_token',
            'course': 'course',
            'assignment': 'assignment',
            'user': 'user',
            'group': 'group',
            'groupset': 'groupset',
        },
    }

    parser = edq.core.argparser.get_default_parser(
            description,
            version = f"v{lms.__version__}",
            include_net = include_net,
            config_options = config_options,
    )

    # Ensure that responses are cleaned as LMS responses.
    if (include_net):
        if (_set_exchanges_clean_func):
            edq.util.net._exchanges_clean_func = edq.util.reflection.get_qualified_name(lms.util.net.clean_lms_response)

    if (include_server):
        parser.add_argument('--server', dest = 'server',
            action = 'store', type = str, default = None,
            help = 'The address of the LMS server to connect to.')

        parser.add_argument('--server-type', dest = 'backend_type',
            action = 'store', type = str,
            default = None, choices = lms.model.constants.BACKEND_TYPES,
            help = 'The type of LMS being connected to (this can normally be guessed from the server address).')

    if (include_auth):
        parser.add_argument('--auth-user', dest = 'auth_user',
            action = 'store', type = str, default = None,
            help = 'The user to authenticate with.')

        parser.add_argument('--auth-password', dest = 'auth_password',
            action = 'store', type = str, default = None,
            help = 'The password to authenticate with.')

        parser.add_argument('--auth-token', dest = 'auth_token',
            action = 'store', type = str, default = None,
            help = 'The token to authenticate with.')

    if (include_course):
        parser.add_argument('--course', dest = 'course',
            action = 'store', type = str, default = None,
            help = 'The course to target for this operation.')

    if (include_assignment):
        parser.add_argument('--assignment', dest = 'assignment',
            action = 'store', type = str, default = None,
            help = 'The assignment to target for this operation.')

    if (include_user):
        parser.add_argument('--user', dest = 'user',
            action = 'store', type = str, default = None,
            help = 'The user to target for this operation.')

    if (include_groupset):
        parser.add_argument('--groupset', dest = 'groupset',
            action = 'store', type = str, default = None,
            help = 'The group set to target for this operation.')

    if (include_group):
        parser.add_argument('--group', dest = 'group',
            action = 'store', type = str, default = None,
            help = 'The group to target for this operation.')

    if (include_output_format):
        parser.add_argument('--format', dest = 'output_format',
            action = 'store', type = str,
            default = lms.model.constants.OUTPUT_FORMAT_TEXT, choices = lms.model.constants.OUTPUT_FORMATS,
            help = 'The format to display the output as (default: %(default)s).')

        parser.add_argument('--skip-headers', dest = 'skip_headers',
            action = 'store_true', default = False,
            help = 'Skip headers when outputting results, will not apply to all formats (default: %(default)s).')

        parser.add_argument('--pretty-headers', dest = 'pretty_headers',
            action = 'store_true', default = False,
            help = 'When displaying headers, try to make them look "pretty" (default: %(default)s).')

        parser.add_argument('--include-extra-fields', dest = 'include_extra_fields',
            action = 'store_true', default = False,
            help = 'Include non-common (usually LMS-specific) fields in results (default: %(default)s).')

    if (include_skip_rows):
        parser.add_argument('--skip-rows', dest = 'skip_rows',
            action = 'store', type = int, default = DEFAULT_SKIP_ROWS,
            help = 'The number of header rows to skip (default: %(default)s).')

    return typing.cast(argparse.ArgumentParser, parser)
