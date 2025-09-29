"""
Customize an argument parser for LMS Toolkit.
"""

import argparse
import typing

import edq.core.argparser

import lms.model.constants

CONFIG_FILENAME: str = 'edq-lms.json'

def get_parser(description: str,
        include_server: bool = True,
        include_token: bool = False,
        include_output_format: bool = False,
        include_course: bool = False,
        include_net: bool = True,
        ) -> argparse.ArgumentParser:
    """
    Get an argument parser specialized for LMS Toolkit.
    """

    config_options = {
        'config_filename': CONFIG_FILENAME,
        'cli_arg_config_map': {
            'server': 'server',
            'backend_type': 'backend_type',
            'token': 'token',
            'course': 'course',
        },
    }

    parser = edq.core.argparser.get_default_parser(
            description,
            include_net = include_net,
            config_options = config_options,
    )

    if (include_server):
        parser.add_argument('--server', dest = 'server',
            action = 'store', type = str, default = None,
            help = 'The address of the LMS server to connect to.')

        parser.add_argument('--server-type', dest = 'backend_type',
            action = 'store', type = str,
            default = None, choices = lms.model.constants.BACKEND_TYPES,
            help = 'The type of LMS being connected to (this can normally be guessed from the server address).')

    if (include_token):
        parser.add_argument('--token', dest = 'token',
            action = 'store', type = str, default = None,
            help = 'The token to authenticate with.')

    if (include_course):
        parser.add_argument('--course', dest = 'course',
            action = 'store', type = str, default = None,
            help = 'The course to target for this operation.')

    if (include_output_format):
        parser.add_argument('--format', dest = 'output_format',
            action = 'store', type = str,
            default = lms.model.constants.OUTPUT_FORMAT_TEXT, choices = lms.model.constants.OUTPUT_FORMATS,
            help = 'The format to display the outut as (default: %(default)s).')

        parser.add_argument('--skip-headers', dest = 'skip_headers',
            action = 'store_true', default = False,
            help = 'Skip headers when outputting results, will not apply to all formats (default: %(default)s).')

        parser.add_argument('--pretty-headers', dest = 'pretty_headers',
            action = 'store_true', default = False,
            help = 'When displaying headers, try to make them look "pretty" (default: %(default)s).')

    return typing.cast(argparse.ArgumentParser, parser)
